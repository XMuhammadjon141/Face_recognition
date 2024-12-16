import uuid
from django.db import models
import pickle  # For storing face encodings

Status_Choice = (
    ('admin', "Admin"),
    ('user', "User"),
)

class UserData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=Status_Choice, default='user')
    is_active = models.BooleanField(default=True)
    face_encoding = models.BinaryField()  # Store face encodings as binary data
    image = models.ImageField(upload_to='user_faces/', null=True, blank=True)  # Store face image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Optional Meta class for custom table name and verbose names
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user_data'  # Explicit table name (optional)

