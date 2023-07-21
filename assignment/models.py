import uuid
from django.template.defaultfilters import slugify

from django.db import models
from account.models import UserProfile

from ckeditor.fields import RichTextField


class Group(models.Model):
    admin = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='group_admin', null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    created_date = models.DateField(auto_now_add=True)
    group_uuid = models.CharField(max_length=10, unique=True, editable=False)
    members = models.ManyToManyField(UserProfile, related_name='group_member', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.group_uuid:
            self.group_uuid = uuid.uuid4().hex[:7]
        if not self.slug:
            self.slug = slugify(self.name)
        print(self.slug)
        return super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    question = RichTextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    post_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"Task posted on {self.post_date}"
