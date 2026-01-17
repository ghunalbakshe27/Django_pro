from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from backend.models import Song, customuser
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import json

User = customuser

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
    return render(request, 'backend/arjit.html')

@login_required(login_url='user_login')
def bhajan(request):
    return render(request, 'backend/bhajan.html')

@login_required(login_url='user_login')
def drivelist(request):
    return render(request, 'backend/drivelist.html')

@login_required(login_url='user_login')
def genres(request):
    return render(request, 'backend/genres.html')

@login_required(login_url='user_login')
def honeys(request):
    return render(request, 'backend/honeys.html')

@login_required(login_url='user_login')
def indianhits(request):
    return render(request, 'backend/indianhits.html')

@login_required(login_url='user_login')
def mixlist(request):
    return render(request, 'backend/mixlist.html')

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
    return render(request, 'backend/phonk.html')

@login_required(login_url='user_login')
def punjabi_hits(request):
    return render(request, 'backend/punjabi hits.html')

@login_required(login_url='user_login')
def subh1(request):
    return render(request, 'backend/subh1.html')

@login_required(login_url='user_login')
def top(request):
    top_songs = Song.objects.filter(category='top').order_by('-release_date')[:12]
    
     # Debug: Check if songs exist and have audio files
    print(f"Found {top_songs.count()} top songs")
    for song in top_songs:
        print(f"Song: {song.title}, Has audio: {bool(song.audio_file)}")

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
    return render(request, 'backend/topeng.html')

@login_required(login_url='user_login')
def romantic_vibes(request):
    return render(request, 'backend/romantic_vibes.html')


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