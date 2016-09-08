from django.conf.urls import include, url
from django.contrib import admin
from page.views import view_home,download_pdf
urlpatterns = [
    # Examples:
    # url(r'^$', 'freelancer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^download/(?P<filename>[\w-]+)/$', download_pdf, name='download'),
    url(r'^',view_home),


]
