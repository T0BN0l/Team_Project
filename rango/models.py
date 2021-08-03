from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    MAX_NAME_LENGTH = 128
    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to='category_images', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    MAX_TITLE_LENGTH = 128
    MAX_URL_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='page_images', blank=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class UserViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128,default='')
    url = models.URLField(default='')

    def __str__(self):
        return self.user.username + ' recently viewed on ' + self.title


class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.user.username + ' recently liked ' + self.liked_title
