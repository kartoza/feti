import urllib.request
from urllib.parse import unquote
import weasyprint
import os
import json
import smtplib
from rest_framework.views import APIView
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
from feti.models.campus import Campus
from feti.models.url import URL
from feti.views.api import (
    ApiCourse,
    ApiCampus
)


class SharingMixin(object):
    """Mixin class to query campus and download map"""
    courses_name = []

    def get_course_names(self):
        return self.courses_name

    def get_campus(self, provider, query):
        api = None
        # Get data
        if provider == 'provider':
            api = ApiCampus()
        elif provider == 'course':
            api = ApiCourse()
        if api:
            campuses = api.filter_model(query)
            self.courses_name = api.courses_name
            return campuses
        return None

    def download_map(self, filename, markers):
        osm_static_url = 'http://staticmap.openstreetmap.de/staticmap.php?center=-30.5,24&' \
                         'zoom=6&size=865x512&maptype=mapnik'
        if markers:
            osm_static_url += '&markers='+markers
        path = os.path.join(settings.MEDIA_ROOT, filename)

        # Check if file already exists
        if not default_storage.exists(path):
            try:
                urllib.request.urlretrieve(osm_static_url, path)
            except urllib.error.URLError:
                raise Http404(
                    'File not found'
                )


class PDFDownload(TemplateView, SharingMixin):
    template_name = 'feti/pdf_template.html'

    def url_fetcher(self, url):
        if url.startswith('assets:'):
            url = url[len('assets:'):]
            url = "file://" + safe_join(settings.MEDIA_ROOT, url)
        return weasyprint.default_url_fetcher(url)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a pdf report

        :param context:
        :param response_kwargs: Keyword arguments
        :return: HTTPResponse
        """

        slug = self.kwargs.get('provider', None)
        query = self.kwargs.get('query', None)
        campuses = self.get_campus(provider=slug, query=query)
        course_names = self.get_course_names()

        markers = ''
        for idx, campus in enumerate(campuses):
            markers += '%s,%s,bluelight%s|' % (campus.location.y, campus.location.x, str(idx))

        filename = '%s-%s.png' % (query, slug)

        self.download_map(filename=filename, markers=markers)

        template = get_template("feti/pdf_template.html")

        if course_names:
            query = ", ".join(course_names)

        context = {
            "type": "pdf",
            "image": filename,
            "title": "Feti Report",
            "provider": slug,
            "query": query,
            "campuses": campuses
        }

        html = template.render(RequestContext(self.request, context))
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % query
        weasyprint.HTML(string=html, url_fetcher=self.url_fetcher).write_pdf(response)

        return response


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

        subject, from_email, to = 'Feti Report', \
                                  email_host, \
                                  [email_address]

        htmly = get_template(self.template_name)
        filename = '%s-%s.png' % (query, provider)
        markers = ''
        for idx, campus in enumerate(campuses):
            markers += '%s,%s,bluelight%s|' % (campus.location.y, campus.location.x, str(idx))

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
        random = get_random_string()
        while URL.objects.filter(random_string=random).exists():
            random = get_random_string()

        if URL.objects.filter(url=url).exists():
            return URL.objects.filter(url=url).first().random_string

        u = URL(
            url=url,
            random_string=random
        )
        u.save()
        return random

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
