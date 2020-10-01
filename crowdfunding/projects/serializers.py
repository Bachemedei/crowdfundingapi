from rest_framework import serializers
from .models import Project, Pledge, PetTag, Shelter


class ShelterSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    address = serializers.CharField(max_length=200)
    charityregister = serializers.IntegerField()
    species = serializers.SlugRelatedField(many=True, slug_field="petspecies", queryset=PetTag.objects.all())
    owner = serializers.ReadOnlyField(source='owner.email')
    def create(self, validated_data):
        species = validated_data.pop('species')
        Shelter.objects.create(**validated_data)
        Shelter.species.set(species)
        Shelter.save()
        return Shelter

class ShelterDetailSerializer(ShelterSerializer):

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.address = validated_data.get('address', instance.address)
        instance.charityregister = validated_data.get('charityregister', instance.name)
        instance.species.set(validated_data.get('species', instance.species))
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.ReadOnlyField(source='supporter.email')
    project_id = serializers.IntegerField()
    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.email')
    shelter = serializers.ReadOnlyField(source='owner.shelter.name')
    is_approved = serializers.ReadOnlyField(source='owner.shelter.is_approved')
    species = serializers.SlugRelatedField(many=True, slug_field="petspecies", queryset=PetTag.objects.all())
    pledges = PledgeSerializer(many=True, read_only=True)

    def create(self, validated_data):
        species = validated_data.pop('species')
        project = Project.objects.create(**validated_data)
        project.species.set(species)
        project.save()
        return project

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.species.set(validated_data.get('species', instance.species))
        instance.save()
        return instance


class PetsSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    petspecies = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return PetTag.objects.create(**validated_data)