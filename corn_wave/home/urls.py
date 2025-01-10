from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import index, user_logout, login_view, registration_view, profile_view
from .forms import RegistrationForm



urlpatterns = [
    path('index/', index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('tours/', views.tour_page, name='tours'),
    path('music/', views.music, name='music'),
    path('tours/', views.tour_page, name='tour'),
    path('registration/', registration_view, name='registration'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile_page'),
    path('Tracks/', views.Tracks, name='Tracks'),
    path('tracks/<int:track_id>/', views.track_detail, name='track_detail'),
    path('upload_track/', views.my_view, name='upload_track'),
    path('track/delete/<int:track_id>/', views.delete_track, name='delete_track'),
    path('favorites/', views.favorites_view, name='favorites_view'),
    path('favorites/add/<int:track_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:track_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/clear/', views.clear_favorites, name='clear_favorites'),
    path('delete_track/<int:track_id>/', views.delete_track, name='delete_track'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:track_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:track_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('success/', views.success_view, name='success'),
    path('add_like/<int:track_id>/', views.add_like, name='add_like'),
    path('remove_like/<int:track_id>/', views.remove_like, name='remove_like'),
    path('add_dislike/<int:track_id>/', views.add_dislike, name='add_dislike'),
    path('remove_dislike/<int:track_id>/', views.remove_dislike, name='remove_dislike'),
    path('search/', views.search, name='search_results'),
    path('Corn_wave', views.Corn_wave, name='corn_wave'),
    path('track/<int:track_id>/add_comment/', views.add_comment, name='add_comment'),





]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
