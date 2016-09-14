from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django.utils._os import safe_join
from django.conf import settings
import urllib.request
import weasyprint
import os
from feti.models.campus import Campus
from django.core.files.storage import default_storage


class PDFDownload(TemplateView):
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
        campuses = Campus.objects.filter(location__isnull=False)

        # Get data
        if slug == 'provider':
            campuses = campuses.filter(
                provider__primary_institution__icontains=query
            )
        elif slug == 'course':
            campuses = campuses.distinct().filter(
                courses__course_description__icontains=query
            )

        markers = ''
        for idx, campus in enumerate(campuses):
            markers += '%s,%s,bluelight%s|' % (campus.location.y,campus.location.x, str(idx))

        # Download images
        osm_static_url = 'http://staticmap.openstreetmap.de/staticmap.php?center=-30.5,24&' \
                         'zoom=6&size=865x512&maptype=mapnik'
        if markers:
            osm_static_url += '&markers='+markers
        filename = '%s-%s.png' % (query, slug)
        path = os.path.join(settings.MEDIA_ROOT, filename)

        # Check if file already exists
        if not default_storage.exists(path):
            urllib.request.urlretrieve(osm_static_url, path)

        template = get_template("feti/pdf_template.html")

        context = {
            "image": filename,
            "title": "Feti Report",
            "query": query,
            "campuses": campuses
        }

        html = template.render(RequestContext(self.request, context))
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % query
        weasyprint.HTML(string=html, url_fetcher=self.url_fetcher).write_pdf(response)

        return response
