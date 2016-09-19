from django.core.management.base import BaseCommand

from feti.models.occupation import Occupation
from feti.models.learning_pathway import LearningPathway, Step, StepDetail
from feti.utils import beautify, get_soup, cleaning

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def create_step(data, learning_pathway):
    try:
        step_detail = StepDetail.objects.get(
            title=data['title'],
            detail=data['detail'])
    except StepDetail.DoesNotExist:
        step_detail = StepDetail()
    step_detail.title = data['title']
    step_detail.detail = data['detail']
    step_detail.save()

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


class Command(BaseCommand):
    args = '<args>'

    def handle(self, *args, **options):
        args = list(args)
        if len(args) > 0:
            if args[len(args) - 1].lower() == "true":
                LearningPathway.objects.all().delete()
                Occupation.objects.all().delete()
                Step.objects.all().delete()
                args.pop(len(args) - 1)
            elif args[len(args) - 1].lower() == "false":
                args.pop(len(args) - 1)
        # ----------------------------------------------------------
        # http://ncap.careerhelp.org.za/
        # ----------------------------------------------------------
        character = "abcdefghijklmnopqrstuvwxyz"
        # check if there is input for character range
        if len(args) > 0:
            if args[0].lower() != "true" and args[0].lower() != "false":
                range = args[0].split("-")
                low = character.index(range[0])
                high = character.index(range[len(range) - 1])
                character = character[low:high]
        character_index = 0
        page = 1
        print("GETTING OCCUPATIONS IN http://ncap.careerhelp.org.za/")
        print("----------------------------------------------------------")
        while True:
            while True:
                # get all of list
                print("processing '%s' page %d" % (character[character_index], page))
                html = get_soup('http://ncap.careerhelp.org.za/occupations/alphabetical/%s/page/%s/' %
                                (character[character_index], page))
                items = html.findAll("div", {"class": "SearchResultItem"})
                if len(items) == 0:
                    # if no item
                    break
                elif len(items) >= 1:
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
                            occupation = {}
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
                            content = str(html.find("div", {"class": "BodyPanel642"}))
                            content = content.split("<b>Description</b>")[1]
                            # description
                            occupation['description'] = beautify(content.split("<b>")[0]).get_text()
                            occupation['description'] = cleaning(occupation['description'])

                            # tasks
                            splits = content.split("<b>Tasks</b>")
                            occupation['tasks'] = beautify(splits[1].split("<b>")[0]).get_text() \
                                if len(splits) > 1 else ""
                            occupation['tasks'] = cleaning(occupation['tasks'])

                            # Occupation Regulation
                            splits = content.split("<b>Occupation Regulation</b>")
                            occupation['occupation_regulation'] = beautify(splits[1].split("<b>")[0]).get_text() \
                                if len(splits) > 1 else ""
                            occupation['occupation_regulation'] = cleaning(occupation['occupation_regulation'])

                            # Learning Pathway Description
                            splits = content.split("<b>Learning Pathway Description</b>")
                            occupation['learning_pathway_description'] = beautify(splits[1].split("<a")[0]).get_text() \
                                if len(splits) > 1 else ""
                            occupation['learning_pathway_description'] = cleaning(
                                occupation['learning_pathway_description'])

                            # get learning pathway
                            pathway_button = html.find("a", {"class": "btn_showLearningPathway"})
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
                                                step_content = step_html.find("div", {"class": "pathItemContent"})
                                                title = step_content.b.string
                                                detail = str(step_content).split("<br/>")
                                                detail = detail[len(detail) - 1]

                                                # assign value
                                                step = {}
                                                step['step_number'] = step_number

                                                # cleaning value
                                                step['title'] = cleaning(beautify(title).get_text())
                                                step['detail'] = cleaning(beautify(detail).get_text())
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
                        break
                page += 1
                print("----------------------------------------------------------")
            page = 1
            character_index += 1
            if character_index >= len(character) - 1:
                break
        print("----------------------------------------------------------")
