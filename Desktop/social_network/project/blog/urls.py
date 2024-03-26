from django.urls import path
from . import views 
from .views import *


urlpatterns = [
    path('post_list/', views.post_list, name='post_list'),
    #user
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    # authtokem
    path('api-token-auth/', AuthTokenView.as_view(), name='api_token_auth'),
    # post
    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/post', PostListCreateAPIView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='posts_detail'),
    # comment
    path('coment/', CommentListAPIView.as_view(), name='comment_list'),
    path('coment/post/', CommentCreateAPIView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment_detail'),
    # path('like/', LikeListAPIView.as_view(), name='like_list'),
    # path('like/post/', LikeCreateAPIView.as_view(), name='like_create'),
    # path('like/<int:pk>/', LikeRetrieveUpdateDestroyAPIView.as_view(), name='like_detail'),
    # templates
    path('post_template/', PostTemplateView.as_view(), name='post_template'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_create/', PostListCreateAPIView.as_view(), name='post_create'),
    # celery
    path('users_list/', GenerateRandomUserView.as_view(), name='users_list'),
]
