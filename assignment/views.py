from django.shortcuts import get_object_or_404

from .serializer import GroupSerializer, TaskSerializer
from .models import Group, Task
from .permission import IsGroupAdmin
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.views import APIView


class CreateGroupView(generics.CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "User must be login"}, status.HTTP_401_UNAUTHORIZED)

        serialize = self.serializer_class(data=request.data, context={"request": request})

        if not serialize.is_valid():
            return Response({"Error": "Something went wrong"}, status.HTTP_400_BAD_REQUEST)

        serialize.save()

        return Response({"Message": "Group Created Successfully", "payload": serialize.data}, status.HTTP_201_CREATED)


class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        group_id = request.data.get("group_id")
        group = Group.objects.filter(group_uuid=group_id).first()

        if group:

            group_serializer = GroupSerializer(group, data=request.data, partial=True, context={"request": request})
            group_serializer.is_valid(raise_exception=True)

            if not self.check_user_exists(group):
                group.members.add(request.user.userprofile)
                group.save()
                return Response({"message": "Group Join", "group-detail": group_serializer.data})

            return Response({"message": "Already in the group", "group-detail": group_serializer.data})
        return Response({"error": "Incorrect Group ID"}, status.HTTP_400_BAD_REQUEST)

    def check_user_exists(self, group):
        return group.members.filter(id=self.request.user.userprofile.id).exists()


class ListGroupView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        group_data = GroupSerializer(self.get_queryset(), many=True, context={"request": request})
        return Response({"groups": group_data.data})


class TaskView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsGroupAdmin, ]

    def post(self, request, *args, **kwargs):
        print(kwargs)
        group_slug = kwargs["slug"]
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            group = get_object_or_404(Group, slug=group_slug)
            serializer.save(group=group)
            return Response({"tasks": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        group_slug = self.kwargs["slug"]
        return Task.objects.filter(group__slug=group_slug)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"tasks": serializer.data})
