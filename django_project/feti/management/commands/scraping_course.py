import re
import urllib
import time
from urllib.error import HTTPError, URLError
from django.core.management.base import BaseCommand
from feti.models.course import Course
from feti.models.campus import Campus
from feti.models.provider import Provider
from feti.models.field_of_study import FieldOfStudy
from feti.models.national_qualifications_framework import NationalQualificationsFramework
from feti.models.education_training_quality_assurance import EducationTrainingQualityAssurance
from feti.utils import beautify, cleaning, get_soup
from feti.management.commands.scraping_campus import scrape_campus

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

        # # check current course
        # try:
        #     course = Course.objects.get(
        #         national_learners_records_database=int(data['id']),
        #         course_description=data['title'],
        #         education_training_quality_assurance=education_training_quality_assurance,
        #         national_qualifications_framework=nqf,
        #         field_of_study=fof)
        # except Course.DoesNotExist:

        course = Course()
        course.education_training_quality_assurance = education_training_quality_assurance
        course.national_learners_records_database = int(data['id'])
        course.course_description = data['title']
        course.national_qualifications_framework = nqf
        course.field_of_study = fof
        course.save()
        return course


def process_saqa_qualification_table(table):
    saqa_details = list(filter(None, table.text.split('\n')))
    row_title = {
        'saqa_qual_id': 'SAQA QUAL ID',
        'title': 'QUALIFICATION TITLE',
        'primary_or_delegated': 'PRIMARY OR DELEGATED QUALITY ASSURANCE FUNCTIONARY',
        'nqf_level': 'NQF LEVEL',
        'field': 'FIELD'
    }
    data = {}

    if row_title['saqa_qual_id'] in saqa_details:
        index = saqa_details.index(row_title['saqa_qual_id'])
        data['id'] = saqa_details[index + 2]

    if row_title['title'] in saqa_details:
        index = saqa_details.index(row_title['title'])
        data['title'] = saqa_details[index + 2]

    if row_title['primary_or_delegated'] in saqa_details:
        index = saqa_details.index(row_title['primary_or_delegated'])
        data['primary or delegated qa functionary'] = saqa_details[index + 2]

    if row_title['nqf_level'] in saqa_details:
        index = saqa_details.index(row_title['nqf_level'])
        data['nqf level'] = saqa_details[index + 5]

    if row_title['field'] in saqa_details:
        index = saqa_details.index(row_title['field'])
        data['field'] = saqa_details[index + 3]

    return data


def scraping_course_ncap(start_page=0, max_page=0):
    # ----------------------------------------------------------
    # http://ncap.careerhelp.org.za/
    # ----------------------------------------------------------
    current_page = 1

    if start_page > 1:
        current_page = start_page

    if max_page < start_page:
        return

    print("GETTING COURSES FROM http://ncap.careerhelp.org.za/")
    print("----------------------------------------------------------")
    while True:
        print("processing page %d" % current_page)
        html = get_soup('http://ncap.careerhelp.org.za/qualifications/search/all/learningfield/all/'
                        'nqflevel/all/qualificationtype/all/page/%d' % current_page)
        items = html.findAll("div", {"class": "SearchResultItem"})
        for item in items:
            item_contents = item.text.split('\n')
            course_desc = item_contents[1].lstrip()

            if course_desc.find('No Courses Found') == 0:
                print('Finished scraping courses from saqa')
                return

            # Get saqa qualification id
            regexp = re.compile("SAQA Qualification ID : (.*)$")
            saqa_id = regexp.search(course_desc).group(1).split(',')[0]

            # Check if id already exist in db
            try:
                course = Course.objects.get(national_learners_records_database=saqa_id)
            except Course.DoesNotExist:
                # Open saqa qualification from id
                while True:
                    try:
                        saqa = get_soup('http://regqs.saqa.org.za/viewQualification.php?id=%s' % saqa_id)
                        break
                    except HTTPError as detail:
                        if detail.errno == 500:
                            time.sleep(1)
                            continue
                        else:
                            raise

                # Add course
                tables = saqa.findAll('table')
                if len(tables) == 0:
                    continue
                processed_table = process_saqa_qualification_table(tables[5])
                course = create_course(processed_table)

            # Update campus
            try:
                campus_name = item_contents[2].split('-')[1]
            except IndexError:
                campus_name = ""
            primary_institution = item_contents[2].split('-')[0]

            try:
                provider = Provider.objects.get(
                    primary_institution=primary_institution)
                campus = Campus.objects.get(
                    campus=campus_name, provider=provider)
            except (Campus.DoesNotExist, Provider.DoesNotExist) as e:
                # create campus
                scrape_campus(item)
                provider = Provider.objects.get(
                    primary_institution=primary_institution)
                campus = Campus.objects.get(
                    campus=campus_name, provider=provider)

            campus.courses.add(course)
            campus.save()

        current_page += 1
        if current_page > max_page > 0:
            break
    print("----------------------------------------------------------")


def scraping_course_saqa():
    # ----------------------------------------------------------
    # http://regqs.saqa.org.za/search.php
    # ----------------------------------------------------------
    trying = 0
    increment = 20
    search_result_at_first = 0
    while True:
        print("----------------------------------------------------------")
        print("GETTING COURSE IN http://regqs.saqa.org.za/search.php/")
        print("----------------------------------------------------------")
        url = 'http://regqs.saqa.org.za/search.php'
        values = {"GO": "Go", "searchResultsATfirst": search_result_at_first,
                  "cat": "qual", "view": "list", "QUALIFICATION_TITLE": "",
                  "QUALIFICATION_ID": "", "NQF_LEVEL_ID": "", "NQF_LEVEL_G2_ID": "", "ABET_BAND_ID": "",
                  "SUBFIELD_ID": "", "QUALIFICATION_TYPE_ID": "", "ORIGINATOR_ID": "", "FIELD_ID": "",
                  "ETQA_ID": "",
                  "SEARCH_TEXT": "", "ACCRED_PROVIDER_ID": "", "NQF_SUBFRAMEWORK_ID": "",}
        print("processing %d to %d" % (search_result_at_first, search_result_at_first + increment))
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # data should be bytes
        req = urllib.request.Request(url, data)
        try:
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
                        value = str(tds[1].a.string).strip().lower() if tds[1].a != None else str(
                            tds[1].string).strip()
                        course[key] = cleaning(value)

                        if "title" in tds[0].string.lower():
                            if "title" in course:
                                create_course(course)
            trying = 0
        except (HTTPError, URLError):
            print("connection error, trying again - %d" % trying)
            trying += 1

        if trying == 0 or trying >= 3:
            search_result_at_first += increment


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
        scraping_course_ncap()
