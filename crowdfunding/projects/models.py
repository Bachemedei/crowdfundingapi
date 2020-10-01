from django.contrib.auth import get_user_model
from django.db import models
# from users.models import get_shelter


class PetTag(models.Model):
    petspecies = models.CharField(max_length=200)

    def __str__(self):
        return self.petspecies

class Shelter(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200)
    charityregister = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    species = models.ManyToManyField(
        PetTag,
        related_name = "shelters",
        related_query_name = "shelter"
    )
    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='shelter'
    )
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )
    species = models.ManyToManyField(
        PetTag,
        related_name = "projects",
        related_query_name = "project"
    )

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )