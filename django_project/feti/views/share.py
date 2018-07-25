import urllib.request
from urllib.parse import unquote
import weasyprint
import os
import json
import smtplib
from more_itertools import unique_everseen
from rest_framework.views import APIView
from haystack.query import SQ, SearchQuerySet
from django.views.generic import TemplateView, UpdateView
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import RequestContext, Context
from django.utils.crypto import get_random_string
from django.utils._os import safe_join
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from haystack.inputs import Clean, Exact
from feti.models.campus import Campus
from feti.models.field_of_study import FieldOfStudy
from feti.models.subfield_of_study import SubFieldOfStudy
from feti.models.qualification_type import QualificationType
from feti.models.url import URL

from feti.views.api import (
    ApiCourse,
    ApiSavedCampus
)
from feti.api_views.campus import (
    ApiCampus
)
from feti.api_views.common_search import CommonSearch
from feti.serializers.favorite_serializer import FavoritePDFSerializer


class SharingMixin(object):
    """Mixin class to query campus and download map"""
    courses_name = []

    def get_course_names(self):
        return self.courses_name

    def get_campus(self, provider, query, user=None):
        api = None
        # Get data
        if provider == 'provider':
            sqs = SearchQuerySet()
            sqs = sqs.filter(
                SQ(campus=query) | SQ(campus_provider=query),
                campus_location_is_null='false',
                courses_is_null='false'
            ).models(Campus)
            campus_data = []

            for result in sqs:
                stored_fields = result.get_stored_fields()
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                        campus_location.y, campus_location.x
                    )
                campus_data.append(stored_fields)

            return campus_data
        elif provider == 'course':
            api = ApiCourse()
        elif provider == 'favorites':
            api = ApiSavedCampus()
            return api.filter_model(user=user)
        if api:
            campuses = api.filter_model(query)
            self.courses_name = api.courses_name
            return campuses
        return None

    def download_map(self, filename, markers, provider=None):
        check_existence = True
        osm_static_url = 'http://staticmap.openstreetmap.de/staticmap.php?center=-30.5,24&' \
                         'zoom=5&size=865x512&maptype=mapnik'
        if markers:
            osm_static_url += '&markers=' + markers

        # if provider:
        #     if provider == 'favorites':
        #         check_existence = False

        path = os.path.join(settings.MEDIA_ROOT, filename)

        # Check if file already exists
        # if not check_existence and default_storage.exists(path):
        if default_storage.exists(path):
            os.remove(path)

        if not default_storage.exists(path):
            try:
                urllib.request.urlretrieve(osm_static_url, path)
            except urllib.error.URLError:
                raise Http404('File not found')


class PDFDownload(TemplateView, SharingMixin, CommonSearch, ApiSavedCampus):
    template_name = 'feti/pdf_template.html'

    def render_to_response(self, context, **response_kwargs):
        """

        """
        query, options = self.process_request(self.request.GET.dict())
        resource = self.kwargs.get('resource', None)
        
        if resource == 'provider':
            data = list(self.search_campuses(query, options))
        elif resource == 'course':
            data = self.search_courses(query, options)
        elif resource == 'favorites':
            if self.request.user.is_authenticated():
                favorites = self.filter_model(user=self.request.user, options=options)
                serializer = FavoritePDFSerializer(favorites, many=True)
                data = serializer.data
            else:
                print('not authenticated')

        map_image = 'feti.png'

        markers = ''
        for result in data:
            y, x = result['campus_location'].split(',')
            markers += '%s,%s,ol-marker-blue|' % (y, x)

        context = {
            "type": "pdf",
            "image": map_image,
            "title": "Feti Report",
            "provider": resource,
            "query": query,
            "campuses": data,
            "options": self.advanced_search_options_to_string(options)
        }

        self.download_map(filename=map_image, markers=markers, provider=resource)
        template = get_template("feti/pdf_template.html")

        html = template.render(RequestContext(self.request, context))

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="feti.pdf"'
        weasyprint.HTML(string=html, url_fetcher=self.url_fetcher).write_pdf(response)
        return response

    def url_fetcher(self, url):
        if url.startswith('assets:'):
            url = url[len('assets:'):]
            url = "file://" + safe_join(settings.MEDIA_ROOT, url)
        return weasyprint.default_url_fetcher(url)

    def advanced_search_options_to_string(self, options):
        result = []
        if 'fos' in options:
            field_of_study_class = FieldOfStudy.objects.get(field_of_study_class=options['fos'])
            result.append('Field of study: {}'.format(field_of_study_class))
        if 'sos' in options:
            subfield_of_study_class = SubFieldOfStudy.objects.get(id=int(options['sos']))
            result.append('Subfield of study: {}'.format(subfield_of_study_class))
        if 'qt' in options:
            qualification_type = QualificationType.objects.get(id=int(options['qt']))
            result.append('Qualification type: {}'.format(qualification_type))
        if 'mc' in options:
            result.append('Minimum credits: {}'.format(options['mc']))
        if 'nqf' in options:
            result.append('NQF level: {}'.format(options['nqf']))
        if 'nqsf' in options:
            result.append('NQSF level: {}'.format(options['nqsf']))
        if 'pi' in options:
            if options['pi'] == '1':
                result.append('Public institution')
            elif options['pi'] == '0':
                result.append('Private institution')
        return result


class EmailShare(UpdateView, SharingMixin):
    template_name = 'feti/pdf_template.html'

    def post(self, request, *args, **kwargs):
        data = request.body

        try:
            retrieved_data = json.loads(data.decode("utf-8"))
        except ValueError:
            raise Http404(
                'Error json value'
            )

        email_address = retrieved_data['email']
        provider = retrieved_data['provider']
        query = retrieved_data['query']
        link = retrieved_data['link']
        email_host = 'noreply@kartoza.com'
        campuses = self.get_campus(provider=provider, query=query)

        htmly = get_template(self.template_name)
        filename = '%s-%s.png' % (query, provider)
        markers = ''

        if provider != 'provider':
            email_data = list(
                unique_everseen(
                    [{
                         'campus_provider': x['campus_provider'],
                         'campus_address': x['campus_address'],
                         'campus_website': x['campus_website'],
                         'location': x['campus_location']
                     }
                     for x in campuses])
            )

            for idx, campus in enumerate(email_data):
                location = campus['location'].split(',')
                markers += '%s,%s,bluelight%s|' % (location[0], location[1], str(idx))
            campuses = email_data

        else:
            for idx, campus in enumerate(campuses):
                location = campus['campus_location'].split(',')
                markers += '%s,%s,bluelight%s|' % (location[0], location[1], str(idx))

        subject, from_email, to = 'Feti Report', \
                                  email_host, \
                                  [email_address]

        self.download_map(filename=filename, markers=markers)

        d = Context({
            "type": "email",
            "title": "Feti Report",
            "query": query,
            "provider": provider,
            "campuses": campuses,
            "link": link
        })

        content = htmly.render(d)
        msg = EmailMessage(subject, content, from_email, to)

        msg.content_subtype = 'html'
        try:
            file = default_storage.open(os.path.join(settings.MEDIA_ROOT, filename))
            image = file.read()
            msg.attach(
                filename=filename,
                content=image,
                mimetype='image/png')
            file.close()
            msg.send(fail_silently=False)
        except smtplib.SMTPException:
            raise Http404(
                'Sending email failed'
            )

        return HttpResponse('success')


class ApiRandomString(UpdateView):
    def generate_random_string(self, url):
        """ Generate random string from url and store it to db"""
        try:
            url = URL.objects.get(url=url)
        except URL.DoesNotExist:
            url = URL(url=url)
            url.save()
        return url.random_string

    def post(self, request, *args, **kwargs):
        data = request.body

        try:
            retrieved_data = json.loads(data.decode("utf-8"))
        except ValueError:
            raise Http404(
                'Error json value'
            )
        url = unquote(retrieved_data['url'])
        response = self.generate_random_string(url)

        return HttpResponse(response)


class ApiGetURL(APIView):
    def get(self, request, random):
        if URL.objects.filter(random_string=random).exists():
            return redirect(URL.objects.filter(random_string=random).first().url)
        return redirect('/')
