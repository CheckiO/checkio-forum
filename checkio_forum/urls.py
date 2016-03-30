import urllib

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings

# admin.autodiscover()

class SocialLoginRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return '/social/login/checkio/?' + urllib.urlencode({'next': self.request.GET.get('next', '/')})

urlpatterns = patterns(
    '',
    url(r'^test/exception/', lambda a: a.a.a.a.a),
    url(r'^user/login/', SocialLoginRedirect.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('checkio_forum.custom_spirit.urls', namespace='custom_spirit')),
    url(r'^', include('spirit.urls')),
)

urlpatterns += patterns(
    'django.views.static',
    url(r'^' + settings.STATIC_URL[1:] + '(.*)$',
        'serve',
        dict(document_root=settings.STATIC_ROOT)),
    url(r'^' + settings.MEDIA_URL[1:] + '(.*)$',
        'serve',
        dict(document_root=settings.MEDIA_ROOT)),
)
