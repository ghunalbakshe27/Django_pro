from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from backend.models import Song, customuser, RecentlyPlayed, LikedSong
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.utils import timezone
import json

User = customuser

# 🔥 NEW: Personal Details API
@login_required(login_url='user_login')
def get_personal_details(request):
    user = request.user
    data = {
        'full_name': user.get_full_name() or user.username,
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%B %d, %Y')
    }
    return JsonResponse(data)


# 🔥 NEW: Recent History API
@login_required(login_url='user_login')
def get_recent_history(request):
    recent_songs = RecentlyPlayed.objects.filter(user=request.user).select_related('song')[:20]
    
    data = {
        'songs': [
            {
                'id': item.song.id,
                'title': item.song.title,
                'artist': item.song.artist,
                'cover': item.song.cover_image.url if item.song.cover_image else '/static/backend/images/default-cover.jpg',
                'played_at': item.played_at.strftime('%B %d, %Y'),
                'duration': item.song.duration or '0:00'
            }
            for item in recent_songs
        ]
    }
    return JsonResponse(data)


# 🔥 NEW: Liked Songs API
@login_required(login_url='user_login')
def get_liked_songs(request):
    liked_songs = LikedSong.objects.filter(user=request.user).select_related('song')
    
    data = {
        'songs': [
            {
                'id': item.song.id,
                'title': item.song.title,
                'artist': item.song.artist,
                'cover': item.song.cover_image.url if item.song.cover_image else '/static/backend/images/default-cover.jpg',
                'liked_at': item.liked_at.strftime('%B %d, %Y'),
                'duration': item.song.duration or '0:00'
            }
            for item in liked_songs
        ]
    }
    return JsonResponse(data)


# 🔥 NEW: Toggle Like Song
@login_required(login_url='user_login')
def toggle_like_song(request, song_id):
    if request.method == 'POST':
        try:
            song = Song.objects.get(id=song_id)
            liked_song, created = LikedSong.objects.get_or_create(user=request.user, song=song)
            
            if not created:
                liked_song.delete()
                return JsonResponse({'status': 'unliked', 'message': 'Song removed from liked songs'})
            else:
                return JsonResponse({'status': 'liked', 'message': 'Song added to liked songs'})
        except Song.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Song not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 🔥 NEW: Track Song Play
@login_required(login_url='user_login')
def track_song_play(request, song_id):
    if request.method == 'POST':
        try:
            song = Song.objects.get(id=song_id)
            # Update or create recently played entry
            recent, created = RecentlyPlayed.objects.update_or_create(
                user=request.user,
                song=song,
                defaults={'played_at': timezone.now()}
            )
            return JsonResponse({'status': 'success', 'message': 'Play tracked'})
        except Song.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Song not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# ✅ use Decorator instead of manual check
@login_required(login_url='user_login')
def homepage(request):
    user = request.user
    
    # CREATE FULLNAME (first_name + last_name)
    full_name = f"{user.first_name} {user.last_name}".strip()
    
    # IF THERE IS NO FULL NAME, USE USERNAME
    if not full_name:
        full_name = user.username
    
    context = {
        'username': full_name,  # FULL NAME OF USER
        'email': user.email,
    }
    return render(request, 'backend/homepage.html', context)

@login_required(login_url='user_login')
def aboutus(request):
    return render(request, 'backend/aboutus.html')

@login_required(login_url='user_login')
def arjit(request):
    arjit_songs = Song.objects.filter(category='arjit').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in arjit_songs
    ])
    
    context = {
        'songs': arjit_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/arjit.html', context)

@login_required(login_url='user_login')
def bhajan(request):
    bhajan_songs = Song.objects.filter(category='bhajan').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in bhajan_songs
    ])
    
    context = {
        'songs': bhajan_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/bhajan.html', context)

@login_required(login_url='user_login')
def drivelist(request):
    drivelist_songs = Song.objects.filter(category='drivelist').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in drivelist_songs
    ])
    
    context = {
        'songs': drivelist_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/drivelist.html', context)

@login_required(login_url='user_login')
def honeys(request):
    honeys_songs = Song.objects.filter(category='honeys').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in honeys_songs
    ])
    
    context = {
        'songs': honeys_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/honeys.html', context)

@login_required(login_url='user_login')
def indianhits(request):
    indianhits_songs = Song.objects.filter(category='indianhits').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in indianhits_songs
    ])
    
    context = {
        'songs': indianhits_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/indianhits.html', context)

@login_required(login_url='user_login')
def mixlist(request):
    mixlist_songs = Song.objects.filter(category='mixlist').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in mixlist_songs
    ])
    
    context = {
        'songs': mixlist_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/mixlist.html', context)

@login_required(login_url='user_login')
def new_releases(request):
    new_release_songs = Song.objects.filter(category='new_releases').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in new_release_songs
    ])
    
    context = {
        'songs': new_release_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/new_releases.html', context)

@login_required(login_url='user_login')
def phonk(request):
    phonk_songs = Song.objects.filter(category='phonk').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in phonk_songs
    ])
    
    context = {
        'songs': phonk_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/phonk.html', context)

@login_required(login_url='user_login')
def punjabi_hits(request):
    punjabi_hits_songs = Song.objects.filter(category='punjabi_hits').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in punjabi_hits_songs
    ])
    
    context = {
        'songs': punjabi_hits_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/punjabi_hits.html', context)

@login_required(login_url='user_login')
def subh1(request):
    subh1_songs = Song.objects.filter(category='subh1').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in subh1_songs
    ])
    
    context = {
        'songs': subh1_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/subh1.html', context)

@login_required(login_url='user_login')
def top(request):
    top_songs = Song.objects.filter(category='top').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in top_songs
    ])
    
    context = {
        'songs': top_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/top.html', context)

@login_required(login_url='user_login')
def topeng(request):
    topeng_songs = Song.objects.filter(category='topeng').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in topeng_songs
    ])
    
    context = {
        'songs': topeng_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/topeng.html', context)

@login_required(login_url='user_login')
def romantic_vibes(request):
    romantic_vibes_songs = Song.objects.filter(category='romantic_vibes').order_by('-release_date')[:12]

    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in romantic_vibes_songs
    ])
    
    context = {
        'songs': romantic_vibes_songs,
        'songs_json': songs_json
    }
    return render(request, 'backend/romantic_vibes.html', context)


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'backend/index.html')


@csrf_protect
def user_register(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        
        # Split fullname
        name_parts = fullname.strip().split(' ', 1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Validation
        if not fullname.strip():
            messages.error(request, 'Full name is required!')
            return redirect('ogregister')
            
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('ogregister')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('ogregister')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('ogregister')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('user_login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('ogregister')
    
    return render(request, 'backend/ogregister.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('user_login')