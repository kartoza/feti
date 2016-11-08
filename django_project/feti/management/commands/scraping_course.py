import re
import urllib
import time
from urllib.error import HTTPError, URLError
from django.core.management.base import BaseCommand
from feti.models.course import Course
from feti.models.campus import Campus
from feti.models.provider import Provider
from feti.utils import beautify, cleaning, get_soup, save_html, get_raw_soup, open_saved_html
from feti.management.commands.scraping_campus import scrape_campus

from feti.models.education_training_quality_assurance import (
    EducationTrainingQualityAssurance)
from feti.models.national_qualifications_framework import (
    NationalQualificationsFramework)
from feti.models.field_of_study import FieldOfStudy
from feti.models.subfield_of_study import SubFieldOfStudy
from feti.models.qualification_type import QualificationType
from feti.models.qual_class import QualClass
from feti.models.national_qualification_framework_subframework import \
    NationalQualificationFrameworkSubFramework
from feti.models.abet_band import AbetBand
from feti.models.pre_2009_national_qualifications_framework import \
    Pre2009NationalQualificationsFramework

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def create_or_update_course(data):
    # save to database
    # provider
    if "ID" in data:
        data['id'] = data['ID']

    if "saqa_qual_id" in data:
        data['id'] = data['saqa_qual_id']

    if "title" not in data and "qualification_title" in data:
        data['title'] = data['qualification_title']

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
        if "TBA" not in data['nqf_level'] and "N/A:" not in data['nqf_level']:
            data['nqf_level'] = data['nqf_level'].split(" ")[2]
            try:
                nqf = NationalQualificationsFramework.objects.get(level=int(data['nqf_level']))
            except NationalQualificationsFramework.DoesNotExist:
                nqf = None

        # SubField of study
        sos = None
        if 'subfield' in data:
            subfield = data['subfield']
            try:
                sos = SubFieldOfStudy.objects.get(learning_subfield=subfield)
            except SubFieldOfStudy.DoesNotExist:
                sos = SubFieldOfStudy.objects.create(
                    learning_subfield=subfield
                )

        # Qualification Type
        qt = None
        if 'qualification_type' in data:
            qual_type = data['qualification_type']
            try:
                qt = QualificationType.objects.get(type=qual_type)
            except QualificationType.DoesNotExist:
                qt = QualificationType.objects.create(
                    type=qual_type
                )

        # Qual class
        qc = None
        if 'qual_class' in data:
            qual_class = data['qual_class']
            try:
                qc = QualClass.objects.get(title=qual_class)
            except QualClass.DoesNotExist:
                qc = QualClass.objects.create(
                    title=qual_class
                )

        # National Qualification Framework Sub-Framework
        nqfs = None
        if 'nqf_sub_framework' in data:
            sub_framework = data['nqf_sub_framework'].split(" - ")
            if len(sub_framework) > 1:
                _title = sub_framework[1]
                _code = sub_framework[0]
                try:
                    nqfs = NationalQualificationFrameworkSubFramework.objects.get(
                        code=_code,
                        title=_title
                    )
                except NationalQualificationFrameworkSubFramework.DoesNotExist:
                    nqfs = NationalQualificationFrameworkSubFramework.objects.create(
                        code=_code,
                        title=_title
                    )

        # Pre-2009 National Qualifications Framework
        pnqf = None
        if 'pre_2009_nqf_level' in data:
            pre_level = data['pre_2009_nqf_level']
            try:
                pnqf = Pre2009NationalQualificationsFramework.objects.get(
                    level=pre_level
                )
            except Pre2009NationalQualificationsFramework.DoesNotExist:
                pnqf = Pre2009NationalQualificationsFramework.objects.create(
                    level=pre_level
                )

        # Abet Band
        aband = None
        if 'abet_band' in data:
            try:
                aband = AbetBand.objects.get(
                    band=data['abet_band']
                )
            except AbetBand.DoesNotExist:
                aband = AbetBand.objects.create(
                    band=data['abet_band']
                )

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

        try:
            course = Course.objects.get(
                national_learners_records_database=int(data['id'])
            )
        except Course.DoesNotExist:
            course = Course.objects.create(
                national_learners_records_database=int(data['id'])
            )

        course.education_training_quality_assurance = education_training_quality_assurance
        course.course_description = data['title']
        course.national_qualifications_framework = nqf
        course.field_of_study = fof
        course.subfield_of_study = sos
        course.qualification_type = qt
        course.qual_class = qc
        course.national_qualifications_subframework = nqfs
        course.pre_2009_national_qualifications_framework = pnqf
        course.abet_band = aband
        course.minimum_credits = int(data['minimum_credits']) if 'minimum_credits' in data else None
        course.registration_status = data['registration_status'] if 'registration_status' in data else None
        course.saqa_decision_number = data['saqa_decision_number'] \
            if 'saqa_decision_number' in data else None
        course.registration_start_date = data['registration_start_date'] \
            if 'registration_start_date' in data else None
        course.registration_end_date = data['registration_end_date'] \
            if 'registration_end_date' in data else None
        course.last_date_for_enrolment = data['last_date_for_enrolment'] \
            if 'last_date_for_enrolment' in data else None
        course.last_date_for_achievement = data['last_date_for_achievement'] \
            if 'last_date_for_achievement' in data else None
        course.purpose_and_rationale_of_the_qualification = data['purpose_and_rationale_of_the_qualification'] \
            if 'purpose_and_rationale_of_the_qualification' in data else None
        course.learning_assumed_to_be_in_place_and_recognition = \
            data['learning_assumed_to_be_in_place_and_recognition_of_prior_learning'] \
            if 'learning_assumed_to_be_in_place_and_recognition_of_prior_learning' in data else None
        course.qualification_rules = data['qualification_rules'] if 'qualification_rules' in data else None
        course.exit_level_outcomes = data['exit_level_outcomes'] if 'exit_level_outcomes' in data else None
        course.associated_assessment_criteria = data['associated_assessment_criteria'] \
            if 'associated_assessment_criteria' in data else None
        course.international_comparability = data['international_comparability'] \
            if 'international_comparability' in data else None
        course.articulation_options = data['articulation_options'] \
            if 'articulation_options' in data else None
        course.moderation_options = data['moderation_options'].lstrip() \
            if 'moderation_options' in data else None
        course.criteria_for_the_registration_of_assessors = \
            data['criteria_for_the_registration_of_assessors'] \
            if 'criteria_for_the_registration_of_assessors' in data else None
        course.reregistration_history = data['reregistration_history'] \
            if 'reregistration_history' in data else None
        course.notes = data['notes'] if 'notes' in data else None

        if 'recognise_previous_learning?' in data:
            course.recognise_previous_learning = True \
                if cleaning(data['recognise_previous_learning?']) == 'Y' \
                else False

        course.save()
        return course


def parse_saqa_qualification_table(table):
    # parse table element to python dictionary

    data = {}
    key_array = []
    value_array = []

    rows = table.findAll('tr')

    for idx, row in enumerate(rows):
        cols = row.findAll('td')
        for col in cols:
            if idx % 2:
                value_array.append(cleaning(col.get_text()))
            else:
                key_array.append(cleaning(col.get_text())
                                 .replace(" ", "_")
                                 .replace("-", "_")
                                 .lower())

    if len(key_array) == len(value_array):
        for i in range(len(key_array)):
            data[key_array[i]] = value_array[i]

    return data


def fetch_from_saqa_form(qualification_id):
    """
    Fetch from saqa search form
    :param qualification_id: Saqa qualification id
    :return: Saqa recorded id
    """
    url = 'http://regqs.saqa.org.za/search.php'
    values = {"GO": "Go", "searchResultsATfirst": 0,
              "cat": "qual", "view": "table", "QUALIFICATION_TITLE": "",
              "QUALIFICATION_ID": qualification_id, "NQF_LEVEL_ID": "", "NQF_LEVEL_G2_ID": "", "ABET_BAND_ID": "",
              "SUBFIELD_ID": "", "QUALIFICATION_TYPE_ID": "", "ORIGINATOR_ID": "", "FIELD_ID": "",
              "ETQA_ID": "",
              "SEARCH_TEXT": "", "ACCRED_PROVIDER_ID": "", "NQF_SUBFRAMEWORK_ID": "", }
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data)
    try:
        with urllib.request.urlopen(req) as response:
            html_doc = response.read()
            html = beautify(html_doc)

            # check emptiness
            items = html.findAll("table")

            if 'No results were found for this search' in str(html):
                return None
            else:
                for table in items:
                    if 'Qualification against which Learning Programme is recorded' in str(table):
                        rows = table.findAll('td')
                        if 'viewQualification' in str(rows[len(rows)-1]):
                            return rows[len(rows)-1].get_text()
                        else:
                            return None
    except (HTTPError, URLError) as e:
        print(e)
        return None


def get_course_detail_from_saqa(qualification_id, no_cache):
    # Get full detail of a course from SAQA
    # http://regqs.saqa.org.za/viewQualification.php?id=<qualification-id>

    print('Qualification ID : {}'.format(qualification_id))
    not_exist_message = 'Details for this qualification are not available'
    saqa_detail = None
    if not no_cache:
        saqa_detail = open_saved_html('saqa-course', qualification_id)

    if not saqa_detail:
        print('No cached sites')
        print('Fetching...')
        while True:
            try:
                saqa_detail = get_raw_soup(
                    'http://regqs.saqa.org.za/viewQualification.php?id=%s' % qualification_id
                )
                if not_exist_message not in str(saqa_detail.content):
                    if not no_cache:
                        save_html('saqa-course', qualification_id, saqa_detail.content)
                    saqa_detail = beautify(saqa_detail.content)
                else:
                    saqa_detail = None
                break
            except HTTPError as detail:
                if detail.errno == 500:
                    time.sleep(1)
                    continue
                else:
                    raise

    if saqa_detail:
        print('Processing html element from saqa...')
        tables = saqa_detail.findAll('table')
        last_idx = 0
        parsed_data = {}
        for idx, table in enumerate(tables):
            if 'SAQA QUAL ID' in table.get_text():
                parsed_data = parse_saqa_qualification_table(table)
                last_idx = idx
                break

        last_title = None
        for table in tables[last_idx+1:len(tables)]:
            if table.find('b'):
                last_title = table.find('b').get_text().replace(' ', '_').lower()
                if last_title not in parsed_data:
                    parsed_data[last_title] = ''
            else:
                if last_title:
                    parsed_data[last_title] = table.get_text().lstrip()
                    last_title = None
        print('Updating course...')
        print('Course updated')
        return create_or_update_course(parsed_data)
    else:
        # Try to search from saqa form
        saqa_id = fetch_from_saqa_form(qualification_id)
        if saqa_id:
            return get_course_detail_from_saqa(saqa_id, no_cache)
        print(not_exist_message)
        print('Course not updated')
    return None


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
                processed_table = parse_saqa_qualification_table(tables[5])
                course = create_or_update_course(processed_table)

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
                                create_or_update_course(course)
            trying = 0
        except (HTTPError, URLError):
            print("connection error, trying again - %d" % trying)
            trying += 1

        if trying == 0 or trying >= 3:
            search_result_at_first += increment


class Command(BaseCommand):
    help = 'Scrapping the courses information'
    args = '<args>'

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            dest='id',
            help='Qualification id'
        )
        parser.add_argument(
            '--re_cache',
            dest='re_cache',
            help='Update html cache'
        )
        parser.add_argument(
            '--no_cache',
            dest='no_cache',
            help='Do not use cached html'
        )

    def handle(self, *args, **options):

        if options['id']:
            no_cache = True if options['no_cache'] else False
            course = get_course_detail_from_saqa(options['id'], no_cache)
        else:
            scraping_course_ncap()
