from django.db.utils import IntegrityError
from feti.models.occupation import Occupation
from feti.models.course import Course
from feti.models.campus import Campus
from feti.models.learning_pathway import LearningPathway, Step, StepDetail
from feti.utils import beautify, get_soup, cleaning
from feti.utilities.scraper.campus_scraper import scrap_campus
from feti.utilities.scraper.course_scraper import get_course_detail_from_saqa

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/01/17'


def process_course_and_provider(html, step_detail):
    """Processing course and provider.

    :param html: html that found
    :type html: str

    :param step_detail: step_detail to be used
    :type step_detail: StepDetail
    """
    body = html.find("div", {"class": "BodyPanel642"})
    if body:
        contents = str(body)
        if 'No Records Found' in contents:
            print('No courses found')
            return
        contents = contents.split('<hr class="hrdivider"/>')
        for content in contents:

            if 'learningprovider' not in content:
                continue

            content_html = beautify(content)
            content_text_list = list(filter(None, content_html.get_text().split('\n')))

            if len(content_text_list) < 2:
                # there is no courses, continue loop
                continue

            provider_url = content_html.find('a').get('href')
            provider_detail = content_text_list[0]
            campus = None

            # Get campus object
            try:
                campus_provider = provider_detail.split(' - ')
                provider_name = campus_provider[0]
                campus_name = '' if len(campus_provider) == 1 else campus_provider[1].strip()
                if campus_name:
                    campus = Campus.objects.get(
                        provider__primary_institution=provider_name,
                        campus__iexact=campus_name)
                else:
                    campus = Campus.objects.filter(
                        provider__primary_institution=provider_name
                    )[0]
            except (Campus.DoesNotExist, IndexError):
                # Create provider with provider url
                campus = scrap_campus(
                    provider_detail,
                    'http://ncap.careerhelp.org.za/' + provider_url)

            if len(content_text_list) > 2:
                for course_detail in content_text_list[2:]:
                    try:
                        saqa_id = course_detail[
                                  course_detail.lower().find('saqa qualification id'): course_detail.find(',')
                                  ].split(':')[1].strip()
                    except IndexError as e:
                        print(e)
                        continue

                    # Get course object
                    try:
                        course = Course.objects.get(
                            national_learners_records_database=saqa_id
                        )
                    except Course.DoesNotExist:
                        # Create a course by saqa id
                        course = get_course_detail_from_saqa(saqa_id, False)

                    if not course:
                        continue
                    if course.course_description == 'National Certificate: N1 Engineering Studies':
                        print(course)

                    print('Add course {}'.format(course.course_description))

                    # If course doesn't exist in campus, then add it
                    if campus and not campus.courses.filter(id=course.id).exists():
                        campus.courses.add(course)

                    # If course doesn't exist in step detail occupation, then add it
                    if not step_detail.course.filter(id=course.id).exists():
                        step_detail.course.add(course)


def create_step(data, learning_pathway):
    """Create step from data.

    :param data: data step that found
    :type data: dict

    :param learning_pathway: learning_pathway that to be used
    :type learning_pathway: LearningPathway
    """
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
    try:
        step.step_number = data['step_number']
        step.learning_pathway = learning_pathway
        step.step_detail = step_detail
        step.save()
    except IntegrityError as e:
        print(e)
        return None

    if 'provider_link' in data:
        # open link
        provider_list_html = get_soup(data['provider_link'])
        if provider_list_html:
            print('Add courses in step detail')
            process_course_and_provider(provider_list_html, step.step_detail)

    return step


def create_learning_pathway(data, occupation):
    """Create learning pathway.

    :param data: data that found
    :type data: dict

    :param occupation: occupation that to be used
    :type occupation: Occupation

    :return: learning pathway that created
    :rtype: LearningPathway
    """
    learning_pathway = LearningPathway()
    learning_pathway.pathway_number = data['pathway_number']
    learning_pathway.occupation = occupation
    learning_pathway.save()
    return learning_pathway


def create_occupation(data):
    """Create occupation.

    :param data: data that found
    :type data: dict

    :return: ocupation that created
    :rtype: Occupation
    """
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
        print('Create learning pathway...')
        pathway = create_learning_pathway(learning_pathway, occupation)
        for step in learning_pathway['steps']:
            print('Create step...')
            create_step(step, pathway)
        pathways.append(pathway)
    return occupation


def scraping_occupations_page(html):
    """Scraping occupation from html.

    :param html: html that found
    :type html: str

    :return: boolean of success
    :rtype: Bool
    """
    items = html.findAll("div", {"class": "SearchResultItem"})
    if len(items) == 0:
        print('this page is empty')
        return False
    else:
        is_empty = False
        # tracing each of item
        for item in items:
            print('--------------------------------')
            if item.string and item.string == "No Records Found.":
                is_empty = True
                print('No records found')
                break
            # get occupation information
            if item.find("a", {"class": "linkNoMore"}):
                pass
            else:
                print('Parsing the occupation list html...')
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
                print('Open learning pathway...')
                html = get_soup(item.a.get('href'))
                body = html.find("div", {"class": "BodyPanel642"})
                if body:
                    print('Parsing learning pathway...')
                    content = str(body)
                    content = content.split("<b>Description</b>")
                    if len(content) > 1:
                        content = content[1]
                        # description
                        occupation['description'] = \
                            cleaning(beautify(content.split("<b>")[0]).get_text())

                        # tasks
                        splits = content.split("<b>Tasks</b>")
                        if len(splits) > 1:
                            occupation['tasks'] = cleaning(beautify(splits[1].split("<b>")[0]).get_text())
                        else:
                            occupation['tasks'] = ""

                        # Occupation Regulation
                        splits = content.split("<b>Occupation Regulation</b>")
                        if len(splits) > 1:
                            occupation['occupation_regulation'] = cleaning(
                                beautify(splits[1].split("<b>")[0]).get_text())
                        else:
                            occupation['occupation_regulation'] = ""

                        # Learning Pathway Description
                        splits = content.split("<b>Learning Pathway Description</b>")
                        if len(splits) > 1:
                            occupation['learning_pathway_description'] = cleaning(beautify(
                                splits[1].split("<a")[0]).get_text())
                        else:
                            occupation['learning_pathway_description'] = ""

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
                                            step = dict()
                                            step['step_number'] = step_number

                                            # check if there is a provider link
                                            if step_content.find('a'):
                                                step['provider_link'] = step_content.find('a').get('href')

                                            # cleaning value
                                            step['title'] = cleaning(beautify(title).get_text())
                                            step['detail'] = cleaning(beautify(detail).get_text())

                                            # get providers that offer this qualification
                                            if step_content.find('a'):
                                                step['provider_link'] = step_content.find('a').get('href')

                                            steps.append(step)
                                            step_number += 1

                                        pathway = {
                                            'pathway_number': pathway_number,
                                            'steps': steps
                                        }
                                        pathways.append(pathway)
                                        pathway_number += 1

                                occupation['learning_pathways'] = pathways

                        print('Update or create for occupation {}'.format(occupation['occupation']))
                        # set to database
                        create_occupation(occupation)
        if is_empty:
            return False
    return True


def scrap_occupations(char=None, limitpage=None):
    # ----------------------------------------------------------
    # http://ncap.careerhelp.org.za/
    # ----------------------------------------------------------
    character = "abcdefghijklmnopqrstuvwxyz"

    # check if there is input for character range
    if char:
        char_range = char.split("-")
        low = character.index(char_range[0])
        high = character.index(char_range[len(char_range) - 1])
        character = character[low:high]

    limit_page = 0

    if limitpage and limitpage.isdigit():
        limit_page = limitpage
    page = 1

    print("GETTING OCCUPATIONS IN http://ncap.careerhelp.org.za/")

    # For testing, get occupations from engineer page
    # html = get_soup('http://ncap.careerhelp.org.za/occupations/search/engineer/page/1/')
    # status = scraping_occupations(html=html)

    for char in character:
        while True:
            # get all of list
            print("processing '%s' page %d" % (char, page))
            html = get_soup('http://ncap.careerhelp.org.za/occupations/alphabetical/%s/page/%s/' %
                            (char, page))
            status = scraping_occupations_page(html)
            if not status:
                break
            page += 1
            if page > limit_page > 0:
                break

            print("----------------------------------------------------------")
        page = 1
    print("----------------------------------------------------------")
