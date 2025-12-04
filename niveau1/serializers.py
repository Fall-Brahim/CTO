from rest_framework import serializers
from .models import Movement, CustomUser, ProfileSportif, Question, Answer, UserResponse, MovementInstruction, Movement
from django.conf import settings

from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Les nouveaux mots de passe ne correspondent pas."}
            )
        return attrs


class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = '__all__'


class ProfileSportifSerializer(serializers.ModelSerializer):
    mouvements = MovementSerializer(many=True, read_only=True)

    class Meta:
        model = ProfileSportif
        fields = ['id', 'level', 'objectif', 'douleur', 'mouvements', 'created_at']



class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.StringRelatedField(many=True, read_only=True)  # Liste des réponses liées

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'answers']

# ---------------------------------------------------------
# Serializer pour Answer
# ---------------------------------------------------------
class AnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.ReadOnlyField(source='question.text')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_text', 'text', 'value']

# ---------------------------------------------------------
# Serializer pour UserResponse
# ---------------------------------------------------------
class UserResponseSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    question_text = serializers.ReadOnlyField(source='question.text')
    answer_text = serializers.ReadOnlyField(source='answer.text')

    class Meta:
        model = UserResponse
        fields = ['id', 'user', 'user_username', 'question', 'question_text', 'answer', 'answer_text']

# ---------------------------------------------------------
# Serializer pour MovementInstruction
# ---------------------------------------------------------
class MovementInstructionSerializer(serializers.ModelSerializer):
    movement_name = serializers.ReadOnlyField(source='movement.name')

    class Meta:
        model = MovementInstruction
        fields = ['id', 'movement', 'movement_name', 'level', 'text_instruction']


