"""api_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mdp.views import taskadvancedexport1, taskadvancedexport2, taskadvancedexport3, taskadvancedexport4,qualityadvancedexport1, qualityadvancedexport2,qualityadvancedexport3,qualityadvancedexport4,enrichbasicexport, tasksbasicexport,mdpbasicexport,qualitybasicexport, mdp, contact,about,mdpbasic, mdpadvanced,qualitybasic,qualityadvanced,tasksbasic,tasksadvanced,enrichbasic
##mdpadvancedexport1, mdpadvancedexport2, mdpadvancedexport3, mdpadvancedexport4,

urlpatterns = [
    #url(r'^admin_tools/', include('admin_tools.urls')),
    #url(r'^myadmin/', admin_site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^mdp/', mdp),
    url(r'^contact/', contact),
    url(r'^about/', about),
    url(r'^mdp-basic/(?P<pk>\d+)/$', mdpbasic),
    url(r'^mdp-basic/(?P<pk>\d+)/export/', mdpbasicexport),
    url(r'^mdpadvanced/', mdpadvanced),
    url(r'^quality-basic/(?P<pk>\d+)/$', qualitybasic),
    url(r'^quality-basic/(?P<pk>\d+)/export/', qualitybasicexport),
    url(r'^qualityadvanced/', qualityadvanced),
    url(r'^quality-advanced/orinclude', qualityadvancedexport1),
    url(r'^quality-advanced/orexclude', qualityadvancedexport2),
    url(r'^quality-advanced/andinclude', qualityadvancedexport3),
    url(r'^quality-advanced/andexclude', qualityadvancedexport4),
    url(r'^tasks-basic/(?P<pk>\d+)/$', tasksbasic),
    url(r'^tasks-basic/(?P<pk>\d+)/export/', tasksbasicexport),
    url(r'taskadvanced/', tasksadvanced),
    url(r'^task-advanced/orinclude', taskadvancedexport1),
    url(r'^task-advanced/orexclude', taskadvancedexport2),
    url(r'^task-advanced/andinclude', taskadvancedexport3),
    url(r'^task-advanced/andexclude', taskadvancedexport4),
    url(r'^enrich-basic/(?P<pk>\d+)/$', enrichbasic),
    url(r'^enrich-basic/(?P<pk>\d+)/export/', enrichbasicexport),
]

urlpatterns += staticfiles_urlpatterns() #Will only work for debug = true

