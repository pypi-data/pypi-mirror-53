from django.views.generic import TemplateView
from django.conf import settings


class WebpackBuiltTemplateView(TemplateView):
    """
    Base built template view
    """
    template_name = "frontend/built.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WebpackBuiltTemplateView, self).get_context_data(*args,
                                                                         **kwargs)
        context['COOKIE_DOMAIN'] = settings.COOKIE_DOMAIN
        context['DJANGO_SSO_DEFAULT_REFERRER'] = settings.DJANGO_SSO_DEFAULT_REFERRER
        return context
