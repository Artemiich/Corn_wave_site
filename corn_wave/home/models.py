from django.db import models
from django.shortcuts import redirect, render


from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    about = models.TextField(verbose_name='Обо мне',
                             null=True, blank=True)
    image = models.ImageField(verbose_name='Фото пользователя',
                              upload_to='profiles/images/')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'




class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)  # Optional album
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    duration = models.DurationField()
    audio_file = models.FileField(upload_to='audio/')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)



    def __str__(self):
        return {self.title}

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'

class Like(models.Model):
    track = models.OneToOneField(Track, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')

class Dislike(models.Model):
    track = models.OneToOneField(Track, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    track = models.ForeignKey(Track, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' Комментарий от {self.user.username} на {self.track.title}'




