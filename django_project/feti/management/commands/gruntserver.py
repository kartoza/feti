import subprocess
import atexit
from django.core.management import call_command
from django.core.management.base import BaseCommand
from core.settings.utils import ABS_PATH


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.grunt_process = None

    def handle(self, *args, **options):
        self.start_grunt()

    def start_grunt(self):
        self.stdout.write('>>> Starting grunt')

        self.grunt_process = subprocess.call([
            'grunt',
            '--gruntfile={0}/Gruntfile.js'.format(ABS_PATH()),
            '--base=.'],
                shell=True)

        self.stdout.write('>>> Collectstatic')
        call_command('collectstatic', verbosity=0, interactive=False)

        def kill_grunt_process(grunt_process):
            self.stdout.write('>>> Closing grunt process')

        atexit.register(kill_grunt_process, self.grunt_process)
