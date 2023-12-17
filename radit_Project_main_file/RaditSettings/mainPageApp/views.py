from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import get_object_or_404
from unidecode import unidecode
import re   
from django.views.decorators.cache import cache_page
from django.db.models import Subquery, OuterRef


from .models import *

def custom_slugify(text):
    result = unidecode(text)
    result = re.sub(r'\s+', '-', result)
    return result

@cache_page(60)
def index(request):
    comments_list = CreateNewRadit.objects.annotate(like_count=Count('likes'), comment_detail_count=Subquery(CommentDetail.objects.filter(comment=OuterRef('pk')).values('comment').annotate(comment_count=Count('pk')).values('comment_count')[:1]
        )).order_by('-like_count')

    items_per_page = 10
    paginator = Paginator(comments_list, items_per_page)

    page = request.GET.get('page')

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)


    context = {
        'comments': comments,
    }

    return render(request, 'mainPageApp/index.html', context)


def logoutView(request):
    logout(request)
    return redirect('mainPageApp:index')


def reviewsAboutSite(request):
    if request.method == 'POST':
        text = request.POST.get('text')

        if request.user.is_authenticated:
            ReviewsAboutSite.objects.create(user=request.user, text=text)
            return redirect('mainPageApp:reviewsAboutSite')

    comments = ReviewsAboutSite.objects.annotate(like_count=Count('likes')).order_by('-like_count')

    context = {
        'comments': comments
    }

    return render(request, 'mainPageApp/reviewsAboutSite.html', context)


def createNewRaditViews(request):
    if request.method == 'POST':
        disscussion_title = request.POST.get('title-topic-for-disscusion')
        disscussion = request.POST.get('topic-for-disscusion')
        if request.user.is_authenticated:
            if CreateNewRadit.objects.filter(user=request.user, title=disscussion_title).exists():
                return HttpResponse("Тема для обсуждения совпадает с уже существующей. Придумайте другую тему.")
            post_slug = custom_slugify(disscussion_title)
            new_radit = CreateNewRadit.objects.create(user=request.user, title=disscussion_title, text=disscussion, post_slug=post_slug)
            new_radit.save()
            return redirect('mainPageApp:createNewRadit')
        else:
            return redirect('loginPage:loginView')


    comments = CreateNewRadit.objects.filter(user=request.user).annotate(like_count=Count('likes')).order_by('-like_count')
    context = {
        'comments': comments
    }

    return render(request, 'mainPageApp/creteblog.html', context)


def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(CreateNewRadit, id=comment_id, user=request.user)
        comment.delete()
        return redirect('mainPageApp:createNewRadit')


def like(request):
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        object_id = int(request.POST.get('object_id'))
        like_value = int(request.POST.get('like_value', 0))

        model_mapping = {
            'create_new_radit': CreateNewRadit,
            'reviews_about_site': ReviewsAboutSite,
            'comment_detail_likes': CommentDetail,
        }

        model = model_mapping.get(content_type)

        if model is None:
            return HttpResponse("Invalid content type")

        obj = get_object_or_404(model, id=object_id)
        user = request.user

        like, created = Like.objects.get_or_create(
            user=user,
            content_type=ContentType.objects.get_for_model(model),
            object_id=obj.id
        )

        if not created:
            like.like = like_value
            like.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def comment_detail_view(request, user_username, post_slug):
    comment_detail = get_object_or_404(CreateNewRadit, post_slug=post_slug)
    username = comment_detail.user.username

    if request.method == 'POST':
        text = request.POST.get('question')

        if request.user.is_authenticated:
            if text:
                new_comment = CommentDetail.objects.create(
                comment=comment_detail,
                user=request.user,
                text=text,
            )
                new_comment.save()
            return redirect('mainPageApp:comment_detail', user_username=new_comment.user.username, post_slug=new_comment.comment.post_slug)
        else:
            return redirect('loginPage:loginView')

    recent_comments = CommentDetail.objects.filter(comment=comment_detail, user=request.user.id).annotate(like_count=Count('likes')).order_by('-like_count')

    context = {
        'comment_detail' : comment_detail,
        'username' : username,
        'recent_comments': recent_comments,
    }
    return render(request, 'mainPageApp/comment_detail.html', context)


def search_result_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        search_result = CreateNewRadit.objects.filter(title__icontains=search_query)
    else:
        return redirect('mainPageApp:index')

    context = {
        'search_query' : search_query,
        'search_result':search_result,
    }

    return render(request, 'mainPageApp/search_results.html', context)


def profile(request):

    profil = UserProfile.objects.get(user=request.user)


    context = {
        'profil' : profil
    }

    return render(request, 'mainPageApp/profile.html', context)


def add_profile(request):
    user_id = request.user.id
    existing_profile = UserProfile.objects.filter(user_id=user_id).first()

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if existing_profile:
            existing_profile.first_name = first_name
            existing_profile.last_name = last_name
            existing_profile.avatar = avatar
            existing_profile.save()
        else:
            profile = UserProfile(user=request.user, first_name=first_name, last_name=last_name, avatar=avatar)
            profile.save()

        return redirect('mainPageApp:profile')

    return render(request, 'mainPageApp/add_profile.html')



