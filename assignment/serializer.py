from django.urls import reverse
from rest_framework import serializers
from account.models import UserProfile
from .models import Group, Task


class GroupSerializer(serializers.ModelSerializer):
    is_teacher = serializers.BooleanField(required=False)
    is_cr = serializers.BooleanField(required=False)
    admin = serializers.SerializerMethodField(method_name="get_admin_username")
    members = serializers.SerializerMethodField(method_name="get_member_usernames")
    group_url = serializers.SerializerMethodField(method_name="get_group_url")

    class Meta:
        model = Group
        fields = ['admin', 'name', 'created_date', 'group_uuid', 'members', 'is_cr', 'is_teacher', 'slug', "group_url"]
        read_only_fields = ["created_date", "group_uuid", "members", "admin", "slug", "group_url"]

    def get_admin_username(self, obj: Group):
        if obj.admin:
            return obj.admin.user.get_username()
        return None

    def get_member_usernames(self, obj: Group):
        if obj.members.exists():
            return [member.user.username for member in obj.members.all()]
        return []

    def get_group_url(self, obj: Group):
        request = self.context.get("request")
        if request is not None:
            group_slug = obj.slug
            return request.build_absolute_uri(reverse("assignment:group_task", kwargs={"slug": group_slug}))

        return None

    def create(self, validated_data):
        is_teacher = validated_data.pop("is_teacher")
        is_cr = validated_data.pop("is_cr")
        user = self.context["request"].user
        group = Group.objects.create(admin=user.userprofile, **validated_data)

        admin_profile = user.userprofile
        admin_profile.is_teacher = is_teacher
        admin_profile.is_cr = is_cr
        admin_profile.save()
        return group


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["question", "post_date", "due_date"]
        read_only_fields = ['posted_date']
