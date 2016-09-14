import urllib.request
import weasyprint
import os
import json
import smtplib
from django.views.generic import TemplateView, UpdateView
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import RequestContext, Context
from django.utils._os import safe_join
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from feti.models.campus import Campus


class SharingMixin(object):
    """Mixin class to query campus and download map"""
    def get_campus(self, provider, query):
        campuses = Campus.objects.filter(location__isnull=False)
        # Get data
        if provider == 'provider':
            campuses = campuses.filter(
                provider__primary_institution__icontains=query
            )
        elif provider == 'course':
            campuses = campuses.distinct().filter(
                courses__course_description__icontains=query
            )
        return campuses

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

        markers = ''
        for idx, campus in enumerate(campuses):
            markers += '%s,%s,bluelight%s|' % (campus.location.y, campus.location.x, str(idx))

        filename = '%s-%s.png' % (query, slug)

        self.download_map(filename=filename, markers=markers)

        template = get_template("feti/pdf_template.html")

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
