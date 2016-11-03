from django.core.management.base import BaseCommand

import os
from difflib import SequenceMatcher
from django.conf import settings
from feti.models.occupation import Occupation
from feti.models.course import Course
from feti.models.campus import Campus
from feti.models.learning_pathway import LearningPathway, Step, StepDetail
from feti.utils import beautify, get_soup, cleaning


__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def get_providers(html):
    step_courses = []
    beautified = beautify(html)
    body = beautified.find("div", {"class": "BodyPanel642"})
    if body:
        contents = str(body)
        contents = contents.split('<hr class="hrdivider"/>')
        for content in contents:
            cleaned = cleaning(content)
            split = list(filter(None, cleaned.split('<br/>')))
            if not beautify(split[0]).find('b'):
                continue
            # get provider

            # get course
            if 'SAQA Qualification ID' in split[2]:
                course_content = split[2]

                # get value inside parenthesis
                value = course_content[course_content.index("(") + 1:course_content.rindex(")")]

                # get id
                course_id = value.split(',')[0].split(':')[1].strip()

                # course title
                course_title = course_content[0: course_content.index("(")].strip()

                course = Course.objects.filter(
                    national_learners_records_database=course_id
                )

                # if there are more than 1 courses, something wrong
                if len(course) > 1:
                    # find the closest one
                    current_ratio = 0
                    correct_course = None

                    for c in course:
                        ratio = SequenceMatcher(None, course_title, c.course_description).ratio()

                        if 0.5 < ratio > current_ratio:
                            # delete course
                            # if correct_course:
                            #     correct_course.delete()
                            correct_course = c

                    if correct_course:
                        step_courses.append(correct_course)

                print(course)
            print(split)
    print(step_courses)


def create_step(data, learning_pathway):
    try:
        step_detail = StepDetail.objects.get(
            title=data['title'],
            detail=data['detail'])
    except StepDetail.DoesNotExist:
        step_detail = StepDetail()
    step_detail.title = data['title']
    step_detail.detail = data['detail']

    if data['provider_link']:
        # open link
        provider_list_html = get_soup(data['provider_link'])
        body = provider_list_html.find("div", {"class": "BodyPanel642"})

        if body:
            content = str(body)

        # iterate on provider list

    # step_detail.save()

    try:
        step = Step.objects.get(
            step_number=data['step_number'],
            learning_pathway=learning_pathway)
    except Step.DoesNotExist:
        step = Step()
    step.step_number = data['step_number']
    step.learning_pathway = learning_pathway
    step.step_detail = step_detail
    step.save()
    return step


def create_learning_pathway(data, occupation):
    learning_pathway = LearningPathway()
    learning_pathway.pathway_number = data['pathway_number']
    learning_pathway.occupation = occupation
    learning_pathway.save()
    return learning_pathway


def create_occupation(data):
    try:
        occupation = Occupation.objects.get(
            occupation=data['occupation'])
    except Occupation.DoesNotExist:
        occupation = Occupation()

    occupation.occupation = data['occupation']
    occupation.green_occupation = data['green_occupation']
    occupation.scarce_skill = data['scarce_skill']
    occupation.description = data['description']
    occupation.tasks = data['tasks']
    occupation.occupation_regulation = data['occupation_regulation']
    occupation.learning_pathway_description = data['learning_pathway_description']
    occupation.save()
    # delete all of it's pathway first
    LearningPathway.objects.filter(occupation=occupation).delete()
    pathways = []
    for learning_pathway in data['learning_pathways']:
        pathway = create_learning_pathway(learning_pathway, occupation)
        for step in learning_pathway['steps']:
            create_step(step, pathway)
        pathways.append(pathway)
    return occupation


def scraping_occupations(html):
    items = html.findAll("div", {"class": "LinkResult"})
    if len(items) == 0:
        print('this page is empty')
        return False
    else:
        is_empty = False
        # tracing each of item
        for item in items:
            if item.string and item.string == "No Records Found.":
                is_empty = True
                break
            # get occupation information
            if item.find("a", {"class": "linkNoMore"}):
                pass
            else:
                occupation = dict()
                occupation['occupation'] = cleaning(item.a.string.split("Occupation Code")[0][:-1])
                occupation['green_occupation'] = False
                occupation['scarce_skill'] = False
                # checking green
                if item.find("span", {"class": "greenTagListView"}):
                    occupation['green_occupation'] = True
                if item.find("span", {"class": "scarceTagListView"}):
                    occupation['scarce_skill'] = True

                # get detail
                html = get_soup(item.a.get('href'))
                body = html.find("div", {"class": "BodyPanel642"})
                if body:
                    content = str(body)
                    content = content.split("<b>Description</b>")
                    if len(content) > 1:
                        content = content[1]
                        # description
                        occupation['description'] = cleaning(beautify(content.split("<b>")[0]).get_text())

                        # tasks
                        splits = content.split("<b>Tasks</b>")
                        occupation['tasks'] = beautify(splits[1].split("<b>")[0]).get_text() \
                            if len(splits) > 1 else ""
                        occupation['tasks'] = cleaning(occupation['tasks'])

                        # Occupation Regulation
                        splits = content.split("<b>Occupation Regulation</b>")
                        occupation['occupation_regulation'] = beautify(splits[1].split("<b>")[0]) \
                            .get_text() \
                            if len(splits) > 1 else ""
                        occupation['occupation_regulation'] = cleaning(occupation['occupation_regulation'])

                        # Learning Pathway Description
                        splits = content.split("<b>Learning Pathway Description</b>")
                        occupation['learning_pathway_description'] = beautify(
                            splits[1].split("<a")[0]).get_text() \
                            if len(splits) > 1 else ""
                        occupation['learning_pathway_description'] = cleaning(
                            occupation['learning_pathway_description'])

                        # get learning pathway
                        pathway_button = html.find("a", {"class": "btn_showLearningPathway"})
                        occupation['learning_pathways'] = []
                        if pathway_button:
                            html = get_soup(pathway_button.get('href'))
                            wrapper = html.find("div", {"id": "tabwrapper"})
                            if wrapper:
                                pathways = []
                                pathways_html = wrapper.findAll("div")
                                pathway_number = 1

                                # check every pathways
                                for pathway_html in pathways_html:
                                    if pathway_html.get('id') and 'pathway' in pathway_html.get('id'):
                                        steps_html = pathway_html.findAll("table")
                                        steps = []
                                        step_number = 1
                                        # get steps
                                        for step_html in steps_html:
                                            step_content = step_html. \
                                                find("div", {"class": "pathItemContent"})
                                            title = step_content.b.string
                                            detail = str(step_content).split("<br/>")
                                            detail = detail[len(detail) - 1]

                                            # assign value
                                            step = {}
                                            step['step_number'] = step_number

                                            # cleaning value
                                            step['title'] = cleaning(beautify(title).get_text())
                                            step['detail'] = cleaning(beautify(detail).get_text())

                                            # get providers that offer this qualification
                                            if step_content.find('a'):
                                                step['provider_link'] = step_content.find('a').get('href')

                                            steps.append(step)
                                            step_number += 1

                                        pathway = {}
                                        pathway['pathway_number'] = pathway_number
                                        pathway['steps'] = steps
                                        pathways.append(pathway)
                                        pathway_number += 1

                                occupation['learning_pathways'] = pathways

                        print(("occupation : %s" % occupation).encode('utf-8'))
                        # set to database
                        create_occupation(occupation)
        if is_empty:
            return False
    return True


class Command(BaseCommand):
    help = 'Scrapping the occupation information'
    args = '<args>'

    def add_arguments(self, parser):
        parser.add_argument(
            '--char',
            dest='char',
            help='Range of character to scrap from ncap list'
        )
        parser.add_argument(
            '--limitpage',
            dest='limitpage',
            help='Page limit'
        )

    def handle(self, *args, **options):

        # ----------------------------------------------------------
        # http://ncap.careerhelp.org.za/
        # ----------------------------------------------------------
        character = "abcdefghijklmnopqrstuvwxyz"

        # check if there is input for character range
        if options['char']:
            char_range = options['char'].split("-")
            low = character.index(char_range[0])
            high = character.index(char_range[len(char_range) - 1])
            character = character[low:high]

        limit_page = 0

        if options['limitpage'] and options['limitpage'].isdigit():
            limit_page = options['limitpage']
        page = 1

        print("GETTING OCCUPATIONS IN http://ncap.careerhelp.org.za/")
        print("----------------------------------------------------------")

        # For testing, get occupations from engineer page
        html = get_soup('http://ncap.careerhelp.org.za/occupations/search/engineer/page/1/')
        # status = scraping_occupations(html=html)

        html_text = open(os.path.join(settings.STATIC_ROOT, 'feti/html/ncap1.html'), 'rb').read()
        get_providers(html_text)

        # for char in character:
        #     while True:
        #         # get all of list
        #         print("processing '%s' page %d" % (char, page))
        #         html = get_soup('http://ncap.careerhelp.org.za/occupations/alphabetical/%s/page/%s/' %
        #                         (char, page))
        #         status = scraping_occupations(html)
        #         if not status:
        #             break
        #         page += 1
        #         if page > limit_page > 0:
        #             break
        #
        #         print("----------------------------------------------------------")
        #     page = 1
        # print("----------------------------------------------------------")
