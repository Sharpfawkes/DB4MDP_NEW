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
    path('intro', views.do_nothing),
    re_path(r'mdpbasic/(?P<pk>\d+)$', views.mdpbasic),
    path('qmbasic/<int:pk>', views.qmbasic),
    path('taskbasic/<int:pk>', views.taskbasic),
    path('lang_mdps/<int:pk>', views.lang_mdps),
    path('lang_langs/<int:pk>', views.lang_langs),
    re_path(r'mdpadvd/$', views.mdpadvanced),
    re_path(r'qmadvd/$', views.qmadvanced),
    re_path(r'taskadvd/$', views.taskadvanced),
    path('enrichbasic/<int:pk>', views.enrichbasic),

]
