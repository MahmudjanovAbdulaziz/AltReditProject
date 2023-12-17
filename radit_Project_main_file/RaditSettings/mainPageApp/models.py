from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Имя Пользователя")
    like = models.IntegerField(default=0)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class CreateNewRadit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Имя Пользователя")
    title = models.CharField(max_length=255)
    text = models.TextField(verbose_name='Текст')
    likes = GenericRelation(Like, related_query_name='create_new_radit_likes')
    post_slug = models.SlugField(unique=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.post_slug})
    
    def __str__(self):
        return f'{self.user.username}-{self.title}'
    
    class Meta:
        verbose_name = "Создать новый редит"
        verbose_name_plural = "Создать новый редит"



class ReviewsAboutSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Имя Пользователя")
    text = models.CharField(max_length=255, verbose_name="Текст")
    likes = GenericRelation(Like, related_query_name='reviews_about_site_likes')
    like = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}-{self.text}'

    class Meta:
        verbose_name = "Комменты о сайте"
        verbose_name_plural = "Комменты о сайте"

class CommentDetail(models.Model):
    comment = models.ForeignKey(CreateNewRadit, on_delete=models.CASCADE, related_name='comment_details')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Имя Пользователя")
    text = models.TextField(verbose_name='Текст')
    likes = GenericRelation(Like, related_query_name='comment_detail_likes')
   
    def __str__(self):
        return f'{self.user.username}-{self.text}'

    class Meta:
        verbose_name = "Детали комментариев"
        verbose_name_plural = "Детали комментариев"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.Case)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    avatar = models.ImageField(upload_to='avatars/')
    
    def __str__(self):
        return f'{self.user.username}-{self.first_name}'
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профиль пользователя"