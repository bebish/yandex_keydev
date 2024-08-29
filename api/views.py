from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password

from .models import Author, Post, Comment, Rating
from .serializer import AuthorSerializer, PostSerializer, CommentSerializer, RatingSerializer
from .send_telegram import send_telegram_message


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    
class RegisterView(APIView):
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['get'])
    def post_detail(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data)


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()  
        data['author'] = request.user.id
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            post = serializer.save()
            self.send_telegram_notification(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_telegram_notification(self, post):
        try:
            telegram_chat_id = post.author.telegram_chat_id
            message = f"Создан новый пост: {post.text}"
            send_telegram_message(telegram_chat_id, message)
        except Exception as e:
            print(f"Ошибка при отправке уведомления в Telegram: {e}")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=['get'])
    def comment_list(self, request, post_id=None):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def comment_add(self, request, post_id=None):
        data = request.data
        data['post'] = post_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @action(detail=True, methods=['post'])
    def mark_add(self, request, post_id=None):
        data = request.data
        data['post'] = post_id
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            rating, created = Rating.objects.update_or_create(
                post_id=post_id,
                user=request.user,
                defaults={'score': data['score']}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
