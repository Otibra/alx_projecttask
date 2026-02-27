from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
     
     PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
     ]

     STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
     
     title = models.CharField(max_length=50)
     description = models.TextField()
     due_date = models.DateTimeField()

     priority_level = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='LOW'
    )

     status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

     user = models.ForeignKey(User, on_delete = models.CASCADE,related_name='tasks')

     def __str__(self):
        return self.title

