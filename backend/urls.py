from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # TEST URLS FOR DEBUGGING PURPOSES
    # path('simple-test/', views.simple_test, name='simple_test'),
    # path('debug-test/', views.debug_test, name='debug_test'),
    # path('db-test/', views.db_test, name='db_test'),
    path('', views.homepage, name='root'),
    # Homepage & Main Pages
    path('homepage/', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    # path('genres/', views.genres, name='genres'),
    path('new-releases/', views.new_releases, name='new_releases'),
    
    # Playlists
    path('top/', views.top, name='top'),
    path('drivelist/', views.drivelist, name='drivelist'),
    path('mixlist/', views.mixlist, name='mixlist'),
    path('romantic_vibes/', views.romantic_vibes, name='romantic_vibes'),
    path('bhajan/', views.bhajan, name='bhajan'),
    path('punjabi-hits/', views.punjabi_hits, name='punjabi_hits'),
    
    # Artists
    path('arjit/', views.arjit, name='arjit'),
    path('honeys/', views.honeys, name='honeys'),
    path('subh1/', views.subh1, name='subh1'),
    
    # Top Charts
    path('topeng/', views.topeng, name='topeng'),
    path('indianhits/', views.indianhits, name='indianhits'),
    path('phonk/', views.phonk, name='phonk'),
    
    # Authentication
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='ogregister'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # 🔥 NEW API Endpoints
    path('api/personal-details/', views.get_personal_details, name='get_personal_details'),
    path('api/recent-history/', views.get_recent_history, name='get_recent_history'),
    path('api/liked-songs/', views.get_liked_songs, name='get_liked_songs'),
    path('api/like-song/<int:song_id>/', views.toggle_like_song, name='toggle_like_song'),
    path('api/track-play/<int:song_id>/', views.track_song_play, name='track_song_play'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

