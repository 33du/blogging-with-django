from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.core.paginator import Paginator
from django.core import serializers
from django.utils import timezone

from .models import Post, Comment, Tag, Image
from .forms import CommentForm
from users.forms import LoginForm, RegistrationForm


def home(request):
    login_form = LoginForm()
    registration_form = RegistrationForm()
    image_posts = Post.objects.all().filter(pub_time__lte=timezone.now()).exclude(image__isnull=True).order_by('-pub_time')[:5]
    image_list = []
    for post in image_posts:
        image_list.append(post.image_set.all()[:1].get())

    recent_posts = Post.objects.all().filter(pub_time__lte=timezone.now()).order_by('-pub_time')[:5]
    recent_comments = Comment.objects.all().order_by('-pub_time')[:5]

    context_objects = {
        'login_form': login_form,
        'registration_form': registration_form,
        'image_list': image_list,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments
    }

    return render(request, 'home.html', context_objects)


def index(request, tag_name=''):
    tag_list = Tag.objects.all()
    login_form = LoginForm()
    registration_form = RegistrationForm()

    if tag_name != '':
        tag_chosen = Tag.objects.get(name=tag_name)
        post_list = tag_chosen.post_set.all().filter(pub_time__lte=timezone.now()).order_by('-pub_time')
    else:
        tag_chosen = None
        post_list = Post.objects.all().filter(pub_time__lte=timezone.now()).order_by('-pub_time')

    paginator = Paginator(post_list, 5)

    if request.is_ajax():
        if request.GET.get('page_number'):
            # Paginate based on the page number in the GET request
            page_number = request.GET.get('page_number');
            try:
                page_objects = paginator.page(page_number).object_list
            except Exception:
                return HttpResponseBadRequest(content_type="text/json")
                # Serialize the paginated objects
            resp = serializers.serialize('json', page_objects)
            return HttpResponse(resp, content_type="text/json")

    else:
        post_list = paginator.page(1).object_list

        context_objects = {
            'login_form': login_form,
            'registration_form': registration_form,
            'post_list': post_list,
            'tag_list': tag_list,
            'tag_chosen': tag_chosen,
        }

        return render(request, 'posts/index.html', context_objects)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment_list = post.comment_set.filter(parent_id=None).order_by('-pub_time')
    login_form = LoginForm()
    registration_form = RegistrationForm()

    try:
        next = Post.objects.all().filter(pub_time__lte=post.pub_time).exclude(id=post_id).order_by('-pub_time')[0:1].get()
    except Post.DoesNotExist:
        next = None

    try:
        prev = Post.objects.all().filter(pub_time__lte=timezone.now(), pub_time__gte=post.pub_time).exclude(id=post_id).order_by('pub_time')[0:1].get()
    except Post.DoesNotExist:
        prev = None


    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            alias = form.cleaned_data['alias']
            post = Post.objects.get(id=post_id)

            if request.user.is_authenticated:
                user = request.user
            else:
                user = None

            if form.cleaned_data['parent_id'] != None:
                parent_id = Comment.objects.get(id=form.cleaned_data['parent_id'])
            else:
                parent_id = None

            try:
                Comment.objects.create(post=post, user=user, text=text, alias=alias, parent_id=parent_id)
            except Exception:
                response = {
                    'has_error': True,
                    'error_msg': "Request failed, please retry."
                }
            else:
                response = {
                    'has_error': False
                }

            return JsonResponse(response)

    else:
        form = CommentForm()

        context_objects = {
            'login_form': login_form,
            'registration_form': registration_form,
            'post': post,
            'form': form,
            'comment_list': comment_list,
            'prev': prev,
            'next': next,
        }
        return render(request, 'posts/detail.html', context_objects)


def delete_comment(request):
    if request.method == 'POST':
        comment_to_delete = Comment.objects.get(id=request.POST['comment_id'])
        if request.user.is_authenticated and request.user == comment_to_delete.user:
            comment_to_delete.delete()
            response = {
                'has_error': False
            }
        elif request.user.is_superuser:
            comment_to_delete.delete()
            response = {
                'has_error': False
            }
        else:
            response = {
                'has_error': True
            }
        return JsonResponse(response)
