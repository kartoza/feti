__author__ = 'christian'

import csv
import logging
from feti.models.campus import Campus as Provider
from feti.models.provider import Provider as PrimaryInstitute

# logging.basicConfig(filename='provider.log')

header = []
original_providers = []
new_providers = []
primary_institutes = []
with open('feti_campus.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = csv_reader.next()[:2]
    for row in csv_reader:
        if row[0] == row[1]:
            # we don't care about these, since we don't need to do anything
            continue
        original_providers.append(row[0])
        new_providers.append(row[1])
        primary_institutes.append(row[3])


message = 'Every duplicate should only be listed once.'
assert len(original_providers) == len(set(original_providers)), message
logging.info('Every duplicate is only listed once')

message = 'We should not want to remove a new institute.'
for original_id in original_providers:
    assert original_id not in new_providers, message

logging.info('No original (where duplicates are moved to) is being removed.')

for original_id, new_id, pi_id in zip(
        original_providers, new_providers, primary_institutes):
    try:
        provider_old = Provider.objects.get(id=original_id)
    except Provider.DoesNotExist:
        print(
            'Cannot remove %s. It may already have been removed' % original_id)
        logging.info(
            'Cannot remove %s. It may already have been removed' % original_id)
        continue
    try:
        provider_new = Provider.objects.get(id=new_id)
    except Provider.DoesNotExist:
        print (
            'Cannot remove %s to %s. '
            'Destination provider does not exist' %
            (original_id, new_id))
        logging.info(
            'Cannot remove %s to %s. '
            'Destination provider does not exist' %
            (original_id, new_id))
        continue
    try:
        pi = PrimaryInstitute.objects.get(id=pi_id)
    except PrimaryInstitute.DoesNotExist:
        print 'Primary institute does not exist.'
        logging.info(
            'Primary institute does not exist.')
        pi = None
        #continue
    if provider_new.provider != pi:
        print 'Destination primary institute does not exist'
        logging.info('Destination primary institute does not exist')
    for course in provider_old.courses.all():
        provider_new.courses.add(course)
        provider_old.courses.remove(course)
        provider_new.save()
        provider_old.save()
    if provider_old.courses.all():
        print 'Could not remove all campuses from provider %s' % (
            original_id)
        logging.info(
            'Could not remove all campuses from provider %s' %
            original_id)
        continue
    provider_old.delete()

