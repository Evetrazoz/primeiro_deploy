from rest_framework import serializers
from .models import Livro
from django.contrib.auth.models import User

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'
class LivroCustomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    titulo = serializers.CharField(max_length=100, required=False)
    autor = serializers.CharField(max_length=100, required=False)
    publicado_em = serializers.DateField(required=False)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username', 'password'
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user