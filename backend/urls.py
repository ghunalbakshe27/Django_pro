from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # TEST URLS FOR DEBUGGING PURPOSES
    # path('simple-test/', views.simple_test, name='simple_test'),
    # path('debug-test/', views.debug_test, name='debug_test'),
    # path('db-test/', views.db_test, name='db_test'),


    path('', views.user_login, name='user_login'),
    path('ogregister/', views.user_register, name='ogregister'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.user_logout, name='user_logout'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('arjit/', views.arjit, name='arjit'),
    path('bhajan/', views.bhajan, name='bhajan'),
    path('drivelist/', views.drivelist, name='drivelist'),
    path('genres/', views.genres, name='genres'),
    path('honeys/', views.honeys, name='honeys'),
    path('indianhits/', views.indianhits, name='indianhits'),
    path('mixlist/', views.mixlist, name='mixlist'),
    path('new-releases/', views.new_releases, name='new_releases'),
    path('phonk/', views.phonk, name='phonk'),
    path('punjabi-hits/', views.punjabi_hits, name='punjabi_hits'),
    path('subh1/', views.subh1, name='subh1'),
    path('top/', views.top, name='top'),
    path('topeng/', views.topeng, name='topeng'),
    path('trend/', views.trend, name='trend'),

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

