# Third-party imports
from precise_bbcode.fields import BBCodeTextField

# Django imports
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# Models
class AdvancedUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активация пройдена?')
    send_messages = models.BooleanField(default=True, verbose_name='Отправлять оповещения на почту?')

    class Meta(AbstractUser.Meta):
        pass


class PostCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:by_category', kwargs={'slug': self.slug})


class Post(models.Model):
    category = models.ForeignKey(PostCategory, on_delete=models.PROTECT, verbose_name='Категория')
    author = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)
    content = BBCodeTextField(null=True, blank=True, verbose_name='Текст поста')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    img = models.ImageField(upload_to='images', blank=True, verbose_name='Фотография')
    is_active = models.BooleanField(default=True, verbose_name='Выводить на сайте?')
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def view(self):
        self.views = models.F('views') + 1
        self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-created_at']

    def __str__(self):
        return '{}.. от {}'.format(self.content[:10], self.author)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.post.id})
