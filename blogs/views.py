from django.shortcuts import render
from .models import Banner,Post, BlogCategory, Comment, FriendlyLink, Tags
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
# Create your views here.

class CommentView(View):
    def get(self, request):
        pass
    def post(self, request, bid):
        comment = Comment()
        comment.user = request.user
        comment.post = Post.objects.get(id=bid)
        comment.content = request.POST.get('content')
        comment.pub_date = datetime.now()
        comment.save()

        return HttpResponseRedirect(reverse("blog_detail", kwargs={"bid":bid}))

#search function
class SearchView(View):
    # def get(self, request):
    #     pass
    def post(self, request):
        kw = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=kw)|Q(content__icontains=kw))

        tags = Tags.objects.all()
        tag_message_list = []
        for t in tags:
            count = len(t.post_set.all())
            tm = TagMessage(t.id, t.name, count)
            tag_message_list.append(tm)

        comment_list = Comment.objects.order_by('-pub_date').all()[:6]
        comment_list1 = []
        post_list1 = []
        for c in comment_list:
            if c.post.id not in post_list1:
                comment_list1.append(c)
                post_list1.append(c.post.id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(post_list, per_page=5, request=request)
        post_list = p.page(page)

        ctx = {
            'post_list': post_list,
            'tags': tag_message_list,
            'comment_list': comment_list1,
        }
        return render(request, 'list.html', ctx)

class TagMessage(object):
    def __init__(self, tid, name, count):
        self.tid = tid
        self.name = name
        self.count = count

#blog detail request
def blog_detail(request,bid):

    post = Post.objects.get(id=bid)
    post.views = post.views + 1
    post.save()

    new_comment_list = Comment.objects.order_by('-pub_date').all()[:6]
    comment_list = post.comment_set.all()

    new_comment_list1 = []
    post_list1 = []
    for c in new_comment_list:
        if c.post.id not in post_list1:
            new_comment_list1.append(c)
            post_list1.append(c.post.id)

    tag_list = post.tags.all()
    post_recomment_list = set(Post.objects.filter(tags__in=tag_list)[:6])

    ctx = {
        'post' : post,
        'new_comment_list': new_comment_list1,
        'post_recomment_list': post_recomment_list,
        'comment_list': comment_list,
    }
    return render(request, 'show.html', ctx)

#list page request
def blog_list(request,cid=-1, tid=-1):
    post_list = None
    if cid != -1:
       cat = BlogCategory.objects.get(id=cid)
       post_list = cat.post_set.all()
    elif tid != -1:
       tag = Tags.objects.get(id=tid)
       post_list = tag.post_set.all()
    else:
       post_list = Post.objects.all()

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(post_list, per_page=5, request=request)
    post_list = p.page(page)

    tags = Tags.objects.all()
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tm = TagMessage(t.id, t.name, count)
        tag_message_list.append(tm)

    comment_list = Comment.objects.order_by('-pub_date').all()[:6]
    comment_list1 = []
    post_list1 = []
    for c in comment_list:
        if c.post.id not in post_list1:
            comment_list1.append(c)
            post_list1.append(c.post.id)

    ctx = {

        'post_list': post_list,
        'tags': tag_message_list,
        'comment_list': comment_list1,

    }
    return render(request, 'list.html', ctx)

#home page request
def index(request):

    banner_list = Banner.objects.all()
    recommend_list = Post.objects.filter(recommend=1)
    post_list = Post.objects.order_by('-pub_date').all()[:3]
    blogcategory_list = BlogCategory.objects.all()
    comment_list = Comment.objects.order_by('-pub_date').all()[:6]
    links = FriendlyLink.objects.all()
    #drop the duplicate comment
    comment_list1 = []
    post_list1 = []
    for c in comment_list:
        if c.post.id not in post_list1:
            comment_list1.append(c)
            post_list1.append(c.post.id)

    ctx = {
        'banner_list': banner_list,
        'recommend_list': recommend_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'comment_list': comment_list1,
        'links': links,
    }

    return render(request,'index.html',ctx)

#CV page(static) request
def cv(request):

    return render(request,'cv.html')
