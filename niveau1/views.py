from django.shortcuts import render

from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Movement, ProfileSportif, Question, Answer, UserResponse, MovementInstruction, CustomUser
from .serializers import UserRegistrationSerializer, UserSerializer, ChangePasswordSerializer, MovementSerializer, ProfileSportifSerializer, QuestionSerializer, AnswerSerializer, UserResponseSerializer, MovementInstructionSerializer
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated



# ---------------------------------------------------------
# ViewSet pour Movement
# ---------------------------------------------------------
class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    # Endpoint optionnel : récupérer les mouvements par nom
    @action(detail=False, methods=['get'])
    def by_name(self, request):
        name = request.query_params.get('name', None)
        if name:
            movements = self.queryset.filter(name__icontains=name)
            serializer = self.get_serializer(movements, many=True)
            return Response(serializer.data)
        return Response({"detail": "Paramètre 'name' requis."}, status=400)

    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Mouvements recommandés selon le profil utilisateur"""
        try:
            profile = ProfileSportif.objects.get(user=request.user)
            # Logique de recommandation basée sur level, objectif, douleur
            movements = Movement.objects.all()  # À affiner selon la logique
            serializer = self.get_serializer(movements, many=True)
            return Response(serializer.data)
        except ProfileSportif.DoesNotExist:
            return Response({'detail': 'Créez d\'abord votre profil'}, status=400)


# ---------------------------------------------------------
# ViewSet pour ProfileSportif
# ---------------------------------------------------------
class ProfileSportifViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get', 'post', 'put'])
    def my_profile(self, request):
        """Gérer le profil sportif de l'utilisateur connecté"""
        if request.method == 'GET':
            try:
                profile = ProfileSportif.objects.get(user=request.user)
                return Response(self.get_serializer(profile).data)
            except ProfileSportif.DoesNotExist:
                return Response({'detail': 'Aucun profil trouvé'}, status=404)
        
        elif request.method in ['POST', 'PUT']:
            profile, created = ProfileSportif.objects.get_or_create(user=request.user)
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        queryset = ProfileSportif.objects.all()
        serializer_class = ProfileSportifSerializer
        filter_CustomUserbackends = [filters.SearchFilter]
        search_fields = ['level', 'objectif', 'douleur']

    # Endpoint optionnel : obtenir tous les mouvements d'un profil
    @action(detail=True, methods=['get'])
    def mouvements(self, request, pk=None):
        profile = self.get_object()
        serializer = MovementSerializer(profile.mouvements.all(), many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'question_type']

    @action(detail=False, methods=['get'])
    def with_answers(self, request):
        """Questions avec leurs réponses"""
        questions = Question.objects.prefetch_related('answers').all()
        data = []
        for q in questions:
            data.append({
                'id': q.id,
                'text': q.text,
                'type': q.question_type,
                'answers': [{'id': a.id, 'text': a.text, 'value': a.value} 
                           for a in q.answers.all()]
            })
        return Response(data)
# ---------------------------------------------------------
# ViewSet pour Answer
# ---------------------------------------------------------
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'value']

# ---------------------------------------------------------
# ViewSet pour UserResponse
# ---------------------------------------------------------
class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'question__text', 'answer__text']

# Endpoint optionnel : récupérer les réponses d’un utilisateur
    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>[^/.]+)')
    def by_user(self, request, user_id=None):
        responses = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(responses, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def submit_questionnaire(self, request):
        """Soumettre toutes les réponses du QCM"""
        responses = request.data.get('responses', [])  # [{question_id, answer_id}, ...]
        created = []
        for resp in responses:
            ur, _ = UserResponse.objects.update_or_create(
                user=request.user,
                question_id=resp['question_id'],
                defaults={'answer_id': resp['answer_id']}
            )
            created.append(ur.id)
        return Response({'created': len(created), 'ids': created})

# ---------------------------------------------------------
# ViewSet pour MovementInstruction
# ---------------------------------------------------------
class MovementInstructionViewSet(viewsets.ModelViewSet):
    queryset = MovementInstruction.objects.all()
    serializer_class = MovementInstructionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movement__name', 'level', 'text_instruction']

# Endpoint optionnel : récupérer les instructions pour un mouvement et un niveau
   
    
    @action(detail=False, methods=['get'])
    def for_me(self, request):
        """Instructions adaptées au niveau de l'utilisateur"""
        movement_id = request.query_params.get('movement')
        try:
            profile = ProfileSportif.objects.get(user=request.user)
            instructions = MovementInstruction.objects.filter(
                movement_id=movement_id,
                level=profile.level
            )
            serializer = self.get_serializer(instructions, many=True)
            return Response(serializer.data)
        except ProfileSportif.DoesNotExist:
            return Response({'detail': 'Créez votre profil'}, status=400)

    @action(detail=False, methods=['get'], url_path='by-movement-level')
    def by_movement_level(self, request):
        movement_id = request.query_params.get('movement')
        level = request.query_params.get('level')
        if movement_id and level:
            instructions = self.queryset.filter(movement_id=movement_id, level=level)
            serializer = self.get_serializer(instructions, many=True)
            return Response(serializer.data)
        return Response({"detail": "Paramètres 'movement' et 'level' requis."}, status=400)



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Inscription d'un nouvel utilisateur"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Récupérer les infos de l'utilisateur connecté"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_me(self, request):
        """Mettre à jour les infos de l'utilisateur connecté"""
        serializer = self.get_serializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Changer le mot de passe"""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Vérifier l'ancien mot de passe
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Mot de passe incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Définir le nouveau mot de passe
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {'message': 'Mot de passe modifié avec succès.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
