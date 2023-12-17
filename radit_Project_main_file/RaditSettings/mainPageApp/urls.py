from django.urls import path


from .views import *

app_name = 'mainPageApp'


urlpatterns = [
    path('', index, name='index'),
    path('reviews/', reviewsAboutSite, name='reviewsAboutSite'),
    path('logout/', logoutView, name='logout'),
    path('createNewRadit/', createNewRaditViews, name='createNewRadit'),
    path('like/', like, name='like'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('comment/<str:user_username>/<slug:post_slug>/', comment_detail_view, name='comment_detail'),
    path('search/', search_result_view, name='search_results'),
    path('profile/', profile, name='profile'),
    path('add_profile/', add_profile, name='add_profile')

]

