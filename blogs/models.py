from django.db import models
from datetime import datetime
from users.models import BlogUser

# Create your models here.

#Rolling picture model
class Banner(models.Model):
    title = models.CharField('headline',max_length=50)
    cover = models.ImageField('rolling picture',upload_to='static/images/banner')
    link_url = models.URLField('image links',max_length=100)
    idx = models.IntegerField('index')
    is_active = models.BooleanField('whether to set to active',default=False)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'rolling picture'
        verbose_name_plural = 'rolling picture'

#Categorize published blogs
class BlogCategory(models.Model):
    name = models.CharField('category name',max_length=20,default='')

    class Meta:
        verbose_name = 'blog classification'
        verbose_name_plural = 'blog classification'
    def __str__(self):
        return self.name

#Category labels
class Tags(models.Model):
    name = models.CharField('label name',max_length=20,default='')

    class Meta:
        verbose_name = 'label'
        verbose_name_plural = 'label'
    def __str__(self):
        return self.name

#
class Post(models.Model):
    user = models.ForeignKey(BlogUser,verbose_name='auther',on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory,verbose_name='blog classification',default=None,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags,verbose_name='label')
    title = models.CharField('headline',max_length=50)
    content = models.TextField('content')
    pub_date = models.DateTimeField('release date',default=datetime.now)
    cover = models.ImageField('blog covers',upload_to='static/images/post',default=None)
    views = models.IntegerField('page view',default=0)
    recommend = models.BooleanField('recommend the blog',default=False)

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blog'
    def __str__(self):
        return self.title

#
class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='blog',on_delete=models.CASCADE)
    user = models.ForeignKey(BlogUser, verbose_name='auther',on_delete=models.CASCADE)
    pub_date = models.DateTimeField('release date')
    content = models.TextField('content')

    def __str__(self):
        return self.content
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comment'

#
class FriendlyLink(models.Model):
    title = models.CharField('headline', max_length=50)
    link = models.URLField('link', max_length=50, default='')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'link'
        verbose_name_plural = 'link'
