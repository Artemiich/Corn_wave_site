from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from .forms import RegistrationForm, LoginForm, HomeTrack, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Track, Favorite, Like, Dislike, Comment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Q



import logging
# Create your views here.


from django.shortcuts import render




def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def music(request):
    return render(request, 'home/music.html')

def tour_page(request):

    return render(request, 'tour_list.html')


def Corn_wave(request):
    return render(request, 'Corn_wave.html')





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(user=user, request=request)
                return redirect('profile_page')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "registration.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect('home')


from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile_view(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
        if created:
            pass
    except Exception as e:
        pass
    return render(request, 'profile.html', {'profile': profile})

def Tracks(request):
    tracks = Track.objects.all()

    for track in tracks:

        Like.objects.get_or_create(track=track)
        Dislike.objects.get_or_create(track=track)


        track.total_likes = track.likes.user.count()
        track.total_dislikes = track.dislikes.user.count()


        track.user_liked = track.likes.user.filter(id=request.user.id).exists()
        track.user_disliked = track.dislikes.user.filter(id=request.user.id).exists()


    return render(request, 'tracks.html', context={'tracks': tracks})






def track_detail(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    audio_url = track.audio_file.url
    comments = Comment.objects.filter(track=track).select_related('user')
    return render(request, 'track_detail.html', {'track': track, 'audio_url': audio_url, 'comments': comments})

def my_view(request):
    if request.method == 'POST':
        form = HomeTrack(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HomeTrack()
    return render(request, 'upload_track.html', {'form': form})




def favorites_view(request):

    favorites = request.session.get('favorites', [])
    tracks = Track.objects.filter(id__in=favorites)
    return render(request, 'favorites_list.html', {'tracks': tracks})

def add_to_favorites(request, track_id):
    favorites = request.session.get('favorites', [])
    if track_id not in favorites:
        favorites.append(track_id)
        request.session['favorites'] = favorites
    return redirect('favorites_view')

def remove_from_favorites(request, track_id):
    favorites = request.session.get('favorites', [])
    if track_id in favorites:
        favorites.remove(track_id)
        request.session['favorites'] = favorites
    return redirect('favorites_view')

def clear_favorites(request):
    request.session['favorites'] = []
    return redirect('favorites_view')



@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'profile_edit.html', context)


def cart_view(request):
    # Получаем корзину из сессии
    cart = request.session.get('cart', {})


    track_ids = cart.keys()
    tracks = Track.objects.filter(id__in=track_ids)


    for track in tracks:
        track.quantity = cart[str(track.id)]

    return render(request, 'cart.html', {'tracks': tracks})


def add_to_cart(request, track_id):

    cart = request.session.get('cart', {})


    cart[str(track_id)] = cart.get(str(track_id), 0) + 1


    request.session['cart'] = cart
    return redirect('cart_view')


def remove_from_cart(request, track_id):
    # Получаем корзину из сессии
    cart = request.session.get('cart', {})


    if str(track_id) in cart:
        cart[str(track_id)] -= 1
        if cart[str(track_id)] <= 0:
            del cart[str(track_id)]


    request.session['cart'] = cart
    return redirect('cart_view')


def clear_cart(request):

    request.session['cart'] = {}
    return redirect('cart_view')



from django.shortcuts import render, redirect
from django.contrib import messages


def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Трек успешно добавлен!")
            return redirect('add_track')
    else:
        form = TrackForm()

    return render(request, 'upload_track.html', {'form': form})

def delete_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    if request.method == 'POST':
        track.delete()
        messages.success(request, "Трек успішно видалено!")
        return redirect('Tracks')  # Змініть на ваше ім'я маршруту для списку треків

    return render(request, 'confirm_delete.html', {'track': track})

def success_view(request):
    return render(request, 'success.html')


@login_required
def delete_track(request, track_id):

    track = get_object_or_404(Track, id=track_id)
    if request.user.is_staff or request.user:
        track.delete()
        messages.success(request, "Трек успешно удалён!")
    else:
        messages.error(request, "У вас нет прав на удаление этого трека.")

    return redirect('Tracks')


from .models import Track






def add_like(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    dislike = Dislike.objects.filter(track=track, user=request.user).first()
    if dislike:
        dislike.user.remove(request.user)
    like, created = Like.objects.get_or_create(track=track)
    like.user.add(request.user)
    return redirect('Tracks')


def remove_like(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    like = get_object_or_404(Like, track=track)
    like.user.remove(request.user)
    return redirect('Tracks')


def add_dislike(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    like = Like.objects.filter(track=track, user=request.user).first()
    if like:
        like.user.remove(request.user)
    dislike, created = Dislike.objects.get_or_create(track=track)
    dislike.user.add(request.user)
    return redirect('Tracks')


def remove_dislike(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    dislike = get_object_or_404(Dislike, track=track)
    dislike.user.remove(request.user)
    return redirect('Tracks')


def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    return render(request, 'track_detail.html', {'track': track})

def search(request):
    query = request.GET.get('q', '')
    tracks = Track.objects.filter(
        Q(title__icontains=query) |
        Q(artist__name__icontains=query) |
        Q(album__title__icontains=query) |
        Q(genre__name__icontains=query)
    ) if query else []

    return render(request, 'search_results.html', {'tracks': tracks, 'query': query})

@login_required
def add_comment(request, track_id):
    if request.method == 'POST':
        track = Track.objects.get(id=track_id)
        content = request.POST.get('content')
        Comment.objects.create(track=track, user=request.user, content=content)
        return redirect('track_detail', track_id=track.id)