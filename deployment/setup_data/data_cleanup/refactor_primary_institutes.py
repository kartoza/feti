__author__ = 'christian'

import csv
import logging
from feti.models.provider import Provider as PrimaryInstitute

logging.basicConfig(filename='primary_institute.log')

header = []
original_primary_institutes = []
new_primary_institutes = []
with open('primary_institution_duplicates.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = csv_reader.next()[:2]
    for row in csv_reader:
        if row[0] == row[1]:
            # we don't care about these, since we don't need to do anything
            continue
        original_primary_institutes.append(row[0])
        new_primary_institutes.append(row[1])

message = 'Every duplicate should only be listed once.'
assert len(original_primary_institutes) == len(set(original_primary_institutes)), message
logging.info('Every duplicate is only listed once')

message = 'We should not want to remove a new institute.'
for original_id in original_primary_institutes:
    assert original_id not in new_primary_institutes, message

logging.info('No original (where duplicates are moved to) is being removed.')

for original_id, new_id in zip(
        original_primary_institutes, new_primary_institutes):
    try:
        pi_old = PrimaryInstitute.objects.get(id=original_id)
    except PrimaryInstitute.DoesNotExist:
        print(
            'Cannot remove %s. It may already have been removed' % original_id)
        logging.info(
            'Cannot remove %s. It may already have been removed' % original_id)
        continue
    try:
        pi_new = PrimaryInstitute.objects.get(id=new_id)
    except PrimaryInstitute.DoesNotExist:
        print(
            'Cannot remove %s to %s. '
            'Destination primary institute does not exist' %
            (original_id, new_id))
        logging.info(
            'Cannot remove %s to %s. '
            'Destination primary institute does not exist' %
            (original_id, new_id))
        continue
    for campus in pi_old.campuses.all():
        campus.provider = pi_new
        campus.save()
    if pi_old.campuses.all():
        print('Could not remove all providers from primary institute %s' %
            original_id)
        logging.info(
            'Could not remove all providers from primary institute %s' %
            original_id)
        continue
    pi_old.delete()

