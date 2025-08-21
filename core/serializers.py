from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, Track

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("username","email","password","nickname")
    def validate_password(self, value):
        validate_password(value); return value
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data); user.set_password(password); user.save(); return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","email","nickname","avatar")

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ("id","title","artist","genre","thumbnail_url","audio_s3_key","duration_sec","is_published","created_at","updated_at")
        read_only_fields = ("id","created_at","updated_at")
