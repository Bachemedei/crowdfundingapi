from rest_framework import serializers
from .models import CustomUser, Profile

from projects.models import PetTag


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    email = serializers.CharField(max_length=200)
    preferredname = serializers.CharField(max_length=200, source='profile.preferredname')
    bio = serializers.CharField(max_length=200, source='profile.bio')
    petlikes = serializers.SlugRelatedField(many=True, slug_field="petspecies", queryset=PetTag.objects.all(), source='profile.petlikes')
    is_supporter = serializers.BooleanField(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('profile')
        pet_likes = profile_data.pop('petlikes')
        new_user = CustomUser.objects.create(**validated_data)
        # update user profile data
        Profile.objects.filter(user=new_user).update(**profile_data)

        # Get Users Profile record
        profile = Profile.objects.get(user=new_user)

        # Add pet likes to the profile
        profile.petlikes.add(*pet_likes)

        # refresh the user
        new_user.refresh_from_db()
        return new_user

    def update(self, user, validated_data):
        print(user)
        print(validated_data)
        user.email = validated_data.get('email', user.email)
        profile_data = validated_data.get('profile')
        if profile_data:
            user.profile.preferredname = profile_data.get('preferredname', user.profile.preferredname)
            user.profile.bio = profile_data.get('bio', user.profile.bio)
            user.profile.petlikes.set(profile_data.get('petlikes', user.profile.petlikes))
        user.save()
        return user
