from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import Project, Pledge, PetTag, Shelter
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, PetsSerializer, ShelterSerializer, ShelterDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsGetOrIsAdmin
from users.models import CustomUser, Profile


# Shelters

class ShelterList(APIView):
    # Create a new shelter, get list of shelters
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        shelters = Shelter.objects.all()
        serializer = ShelterSerializer(shelters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShelterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ShelterDetail(APIView):
    # Get details of a single shelter, update shelter details
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            return Shelter.objects.get(pk=pk)
        except Shelter.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        shelter = self.get_object(pk)
        serializer = ShelterDetailSerializer(shelter)
        return Response(serializer.data)

    def put(self, request, pk):
        shelter = self.get_object(pk)
        data = request.data
        serializer = ShelterDetailSerializer(
            instance=shelter,
            data=data,
            partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UsersShelters(generics.RetrieveAPIView):
    # Get list of all projects associated with shelter in URL
    serializer_class = ShelterDetailSerializer

    def get_object(self):
        user_id = self.kwargs['pk']
        try:
            return Shelter.objects.get(owner=user_id)
        except Shelter.DoesNotExist:
            raise Http404


# Projects

class ProjectList(APIView):
    # Create a new project, get list of projects

    #this permission allows users logged in to create projects and 
    # non logged in users to read project
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.instance
            if not request.user.shelter.is_approved:
                raise ParseError('Shelter is not approved, can not create projects')
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    # See details of single project, update project
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(
            status = status.HTTP_204_NO_CONTENT
        )



# Filtered project lists

class SheltersProjects(generics.ListAPIView):
    # Get list of all projects associated with shelter in URL
    serializer_class = ProjectSerializer

    def get_queryset(self):
        sheltername = self.kwargs['slug']
        shelter = Shelter.objects.get(name=sheltername)
        user = shelter.owner
        return Project.objects.filter(owner=user)

class RecommendedProjects(generics.ListAPIView):
    # Get list of projects for pets that the current user likes
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        user = CustomUser.objects.get(pk=user_id)
        liked_list = user.profile.petlikes.all()
        return Project.objects.filter(species__in=liked_list)

class UsersSupportedProjects(generics.ListAPIView):
    # Get list of projects that the current user has supported
    serializer_class = ProjectSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = CustomUser.objects.get(pk=pk)
        return Project.objects.filter(pledges__supporter=user)


# Pledges

class PledgeList(APIView):
    # Create a pledge, return list of pledges

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        # user = request.user.profile.preferredname
        # print(user)
        if serializer.is_valid():
            # serializer.save(supporter=request.user.profile.preferredname)
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UsersPledges(generics.ListAPIView):
    # Get list of pledges that the current user has made
    serializer_class = PledgeSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = CustomUser.objects.get(pk=pk)
        return Pledge.objects.filter(supporter=user)
    


# Pet Categories

class PetCategory(APIView):
    # Create pet category, return list of all categories
    
    permission_classes = [IsGetOrIsAdmin]

    def post(self, request):
        serializer = PetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request):
        pets = PetTag.objects.all()
        serializer = PetsSerializer(pets, many=True)
        return Response(serializer.data)