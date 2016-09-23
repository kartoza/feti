from django.http import Http404
from django.views.generic import TemplateView

from feti.models.campus import Campus
from feti.models.provider import Provider
from feti.serializers.provider_serializer import ProviderSerializer
from feti.serializers.campus_serializer import CampusSerializer

from user_profile.models.provider_official import ProviderOfficial
from user_profile.models.campus_official import CampusOfficial

from feti.templatetags.user_admin import has_access_user_admin


class UserAdminPage(TemplateView):
    template_name = 'user_admin_page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        campus = None
        providers = None  # get official detail
        user = request.user
        if has_access_user_admin(user):
            try:
                # provider serializer
                if user.is_staff:
                    providers = ProviderSerializer(Provider.objects.all(), many=True).data
                else:
                    official = ProviderOfficial.objects.get(user=user)
                    providers = ProviderSerializer(official.provider.all(), many=True).data
            except ProviderOfficial.DoesNotExist:
                pass

            try:
                # campus serializer
                if user.is_staff:
                    campus = CampusSerializer(Campus.objects.all(), many=True).data
                else:
                    official = CampusOfficial.objects.get(user=user)
                    campus = CampusSerializer(official.campus.all(), many=True).data
            except CampusOfficial.DoesNotExist:
                pass

        if campus or providers:
            if campus:
                context['campus'] = campus
            if providers:
                context['providers'] = providers
            return self.render_to_response(context)
        else:
            raise Http404()
