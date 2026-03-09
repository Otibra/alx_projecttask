# Import Django base model classes
from django.db import models

# Import Django's built-in User model
# This allows projects to belong to a specific user
from django.contrib.auth.models import User


# Project model represents a project created by a user
class Project(models.Model):

    # Stores the project name
    name = models.CharField(max_length=100)

    # ForeignKey relationship to User
    # Each project belongs to one user
    # If the user is deleted, all their projects are deleted
    # related_name='projects' allows: user.projects.all()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    # Automatically records the date/time when the project is created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation used in Django admin and shell
    def __str__(self):
        return self.name


# Task model represents tasks inside a project
class Task(models.Model):

    # Possible priority levels for a task
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    # Possible status values for a task
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    # Task title
    title = models.CharField(max_length=50)

    # Detailed description of the task
    description = models.TextField()

    # Deadline for the task
    due_date = models.DateTimeField()

    # Task priority level
    # Choices restrict allowed values
    # Default priority is LOW
    priority_level = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='LOW'
    )

    # Current task status
    # Default is PENDING
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    # Relationship to Project
    # Each task belongs to one project
    # If the project is deleted, all tasks are deleted
    # related_name='tasks' allows: project.tasks.all()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    # String representation for admin and debugging
    def __str__(self):
        return self.title
    
     