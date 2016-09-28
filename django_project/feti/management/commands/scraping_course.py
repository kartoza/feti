import urllib

from django.core.management.base import BaseCommand
from feti.models.course import Course
from feti.models.field_of_study import FieldOfStudy
from feti.models.national_qualifications_framework import NationalQualificationsFramework
from feti.models.education_training_quality_assurance import EducationTrainingQualityAssurance
from feti.utils import beautify, cleaning

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def create_course(data):
    # save to database
    # provider
    if "ID" in data:
        data['id'] = data['ID']

    if "id" in data:
        print(("insert to database : %s" % data).encode('utf-8'))
        # getting education_training_quality_assurance
        education_training_quality_assurance = None
        if 'primary or delegated qa functionary' in data:
            edu_data = data['primary or delegated qa functionary'].split("-")
            if len(edu_data) == 2 and len(edu_data[0]) <= 30:
                try:
                    education_training_quality_assurance = EducationTrainingQualityAssurance.objects.get(
                        acronym=edu_data[0].strip())
                except EducationTrainingQualityAssurance.DoesNotExist:
                    education_training_quality_assurance = EducationTrainingQualityAssurance()
                    education_training_quality_assurance.acronym = edu_data[0].strip()
                    education_training_quality_assurance.body_name = edu_data[1].strip()
                    education_training_quality_assurance.save()
        # get NQF
        nqf = None
        if "TBA" not in data['nqf level'] and "N/A:" not in data['nqf level']:
            data['nqf level'] = data['nqf level'].split(" ")[2]
            try:
                nqf = NationalQualificationsFramework.objects.get(level=int(data['nqf level']))
            except NationalQualificationsFramework.DoesNotExist:
                nqf = None

        # get FOF
        field = data['field'].replace("0", "").split("-")
        field[0] = cleaning(field[0])
        field_class = int(field[0].split(" ")[1])
        try:
            fof = FieldOfStudy.objects.get(field_of_study_class=field_class)
        except FieldOfStudy.DoesNotExist:
            fof = FieldOfStudy()
            fof.field_of_study_class = field_class
            fof.field_of_study_description = field[1]
            fof.save()

        # check current course
        try:
            course = Course.objects.get(
                national_learners_records_database=int(data['id']),
                course_description=data['title'],
                education_training_quality_assurance=education_training_quality_assurance,
                national_qualifications_framework=nqf,
                field_of_study=fof)
        except Course.DoesNotExist:
            course = Course()

        course.education_training_quality_assurance = education_training_quality_assurance
        course.national_learners_records_database = int(data['id'])
        course.course_description = data['title']
        course.national_qualifications_framework = nqf
        course.field_of_study = fof
        course.save()


class Command(BaseCommand):
    args = '<args>'

    def handle(self, *args, **options):
        args = list(args)
        if len(args) > 0:
            if args[len(args) - 1].lower() == "true":
                Course.objects.all().delete()
                args.pop(len(args) - 1)
            elif args[len(args) - 1].lower() == "false":
                args.pop(len(args) - 1)
        # ----------------------------------------------------------
        # http://regqs.saqa.org.za/search.php
        # ----------------------------------------------------------
        increment = 20
        searchResultsATfirst = 0
        while True:
            print("----------------------------------------------------------")
            print("GETTING COURSE IN http://regqs.saqa.org.za/search.php/")
            print("----------------------------------------------------------")
            url = 'http://regqs.saqa.org.za/search.php'
            values = {"GO": "Go", "searchResultsATfirst": searchResultsATfirst,
                      "cat": "qual", "view": "list", "QUALIFICATION_TITLE": "",
                      "QUALIFICATION_ID": "", "NQF_LEVEL_ID": "", "NQF_LEVEL_G2_ID": "", "ABET_BAND_ID": "",
                      "SUBFIELD_ID": "", "QUALIFICATION_TYPE_ID": "", "ORIGINATOR_ID": "", "FIELD_ID": "",
                      "ETQA_ID": "",
                      "SEARCH_TEXT": "", "ACCRED_PROVIDER_ID": "", "NQF_SUBFRAMEWORK_ID": "",}
            print("processing %d to %d" % (searchResultsATfirst, searchResultsATfirst + increment))
            data = urllib.parse.urlencode(values)
            data = data.encode('ascii')  # data should be bytes
            req = urllib.request.Request(url, data)
            with urllib.request.urlopen(req) as response:
                html_doc = response.read()
                html = beautify(html_doc)

                # check emptiness
                items = html.findAll("table")
                last_table = str(items[len(items) - 1])
                if not "Next" in last_table and not "Prev" in last_table:
                    print("it is empty")
                    break
                # extract courses
                rows = html.findAll('tr')
                course = {}
                for row in rows:
                    tds = row.findAll('td')
                    if len(tds) == 2 and tds[0].string != None:

                        key = str(tds[0].string).replace(":", "").strip().lower()
                        value = str(tds[1].a.string).strip().lower() if tds[1].a != None else str(tds[1].string).strip()
                        course[key] = cleaning(value)

                        if "title" in tds[0].string.lower():
                            if "title" in course:
                                create_course(course)

            searchResultsATfirst += increment
