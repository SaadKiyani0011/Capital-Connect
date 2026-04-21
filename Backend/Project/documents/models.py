from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.owner.id}/{filename}'

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    file_type = models.CharField(max_length=50, blank=True)
    file_size_bytes = models.PositiveIntegerField(null=True, blank=True)
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=50, default='pending') # pending, signed, archived
    is_shared = models.BooleanField(default=False)
    e_signature = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (v{self.version}) - {self.owner.username}"
