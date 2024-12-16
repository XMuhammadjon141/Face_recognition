from django.db import models

Status_Choice = (
    ('admin', "Admin"),
    ('user', "User"),
)


class User_Info(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    status = models.CharField(max_length=100, choices=Status_Choice, default='user')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user_info'

