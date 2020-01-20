"""DB4MDP_NEW URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from mdp import views
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.do_nothing),
    path('mdpbasic/', views.mdpbasic),
    re_path(r'mdpbasic/(?P<pk>\d+)$', views.mdpbasic),
    path('qmbasic/', views.qmbasic),
    re_path(r'qmbasic/(?P<pk>\d+)$', views.qmbasic),
    path('taskbasic/', views.taskbasic),
    re_path(r'taskbasic/(?P<pk>\d+)$', views.taskbasic),
    path('lang_mdps/', views.lang_mdps),
    re_path(r'lang_mdps/(?P<pk>\d+)$', views.lang_mdps),
    path('lang_langs/', views.lang_langs),
    re_path(r'lang_langs/(?P<pk>\d+)$', views.lang_langs),
    path('enrichbasic/', views.enrichbasic),
    re_path(r'enrichbasic/(?P<pk>\d+)$', views.enrichbasic),
    re_path(r'mdpadvd/$', views.mdpadvanced),
    re_path(r'qmadvd/$', views.qmadvanced),
    re_path(r'taskadvd/$', views.taskadvanced),

]
