from rest_framework.routers import DefaultRouter
from .views import MovementViewSet, CustomUserViewSet, ProfileSportifViewSet, QuestionViewSet, AnswerViewSet, UserResponseViewSet, MovementInstructionViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path,include 

router = DefaultRouter()
router.register(r'movements', MovementViewSet, basename="movement")
router.register(r'profiles', ProfileSportifViewSet, basename="profile")
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'user-responses', UserResponseViewSet, basename='user-responses')
router.register(r'movement-instructions', MovementInstructionViewSet, basename='movement-instructions')
router.register(r'users', CustomUserViewSet)

#urlpatterns = router.urls  # renvoie directement toutes les routes du router
urlpatterns = [
    # JWT Authentication endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Router URLs
    path('', include(router.urls)),
]
