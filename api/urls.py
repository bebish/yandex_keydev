from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, PostViewSet, CommentViewSet, RatingViewSet, RegisterView, PostCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'account', AuthorViewSet, basename='account')
router.register(r'post', PostViewSet, basename='post')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/account_register/', RegisterView.as_view(), name='account_register'), 
    path('api/post_add/',PostCreateAPIView.as_view(),name='post_add'), 
    path('api/post/<int:post_id>/comment/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('api/post/<int:post_id>/mark/', RatingViewSet.as_view({'post': 'create'}), name='rating-add'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
