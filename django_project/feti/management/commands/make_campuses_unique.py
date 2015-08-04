from django.core.management.base import BaseCommand, CommandError
from feti.models.campus import Campus

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):

        for primary_campus in Campus.objects.all():
            name = primary_campus.campus
            duplicate_campuses = Campus.objects.filter(
                campus=name)
            count = duplicate_campuses.count()
            duplicate_campuses = list(duplicate_campuses)
            if count > 1:
                self.stdout.write(
                    'There are %s campuses with the name %s.' % (count, name))
                for current_count in xrange(count):
                    current_campus = duplicate_campuses[current_count]
                    current_campus.campus = '%s %s' % (name, current_count + 1)
                    current_campus.save()

        self.stdout.write('All campus names now unique.')