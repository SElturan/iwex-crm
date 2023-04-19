from django.shortcuts import render
from .models import Post
from .models import *
# templates
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from .forms import *
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import generics, filters, status
from .serializers import *
import django_filters
#auth
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# auth
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
#user
from django.contrib.auth.models import User
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
#
# Celery
from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import redirect
from .serializers import *


# celery___________________________________________________________________

class GenerateRandomUserView(FormView):
    template_name = 'posts/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')

# ___

class RegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializers
    
    
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'username': user.username,
                'token': token.key
            }
        )

#_______________________________________________________________________________________________

class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': user.first_name
        })



def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post.html', {'posts': posts})


# Post________________________________________________________________________________________________

class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)
    

class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def update(self, request, *args, **kwargs): # мы тут перепиали на продавца его действия
        isinstance = self.get_object() # проверяем что пользователь является записи
        if isinstance.author == request.user:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You are not the owner this record'})



# Comments_______________________________________________________________________________________________

class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

# Templates__________________________________________________________________________________

class PostTemplateView(ListView):
    template_name = 'posts/post.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.all() # sinemas - должен быть, потому что в темплейтс не будет рендериться
        return context


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.model.objects.get(pk=self.kwargs['pk'])
        return context


class CinemaCreateView(CreateView):
    template_name = 'post/post_create.html'
    form_class = PostForm
    success_url = '/post_detail/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # redirect to movie_detail
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class CinemaUpdateView(UpdateView):
    model = Post
    template_name = 'post/post_update.html'

