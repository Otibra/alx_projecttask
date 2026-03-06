# Import the base Django model classes
from django.db import models
# Import the built-in User model for associating users with projects/tasks
from django.contrib.auth.models import User

# Create your models here

# Define a Project model to represent a project entity
class Project(models.Model):
    # 'name' is a character field to store the project name, max length 100
    name = models.CharField(max_length=100)
    
    # 'user' establishes a relationship to the User model (who owns the project)
    # on_delete=models.CASCADE ensures that if the user is deleted, their projects are deleted too
    # related_name='projects' allows reverse lookup: user.projects.all()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    # 'created_at' automatically stores the timestamp when the project is created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the project; shows the project name in admin and other displays
    def __str__(self):
        return self.name


# Define a Task model to represent tasks within a project
class Task(models.Model):
     
     # Define choices for task priority
     PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
     ]

     # Define choices for task status
     STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
     
     # 'title' stores the task's title, max length 50
     title = models.CharField(max_length=50)
     
     # 'description' stores detailed information about the task
     description = models.TextField()
     
     # 'due_date' stores the deadline for the task
     due_date = models.DateTimeField()

     # 'priority_level' stores the priority of the task
     # choices=PRIORITY_CHOICES limits allowed values
     # default='LOW' sets default priority if not specified
     priority_level = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='LOW'
    )

     # 'status' stores the current status of the task
     # choices=STATUS_CHOICES limits allowed values
     # default='PENDING' sets initial status
     status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

     # 'project' establishes a foreign key relationship to the Project model
     # on_delete=models.CASCADE ensures tasks are deleted if their project is deleted
     # related_name='tasks' allows reverse lookup: project.tasks.all()
     project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name='tasks')

     # String representation of the task; shows the task title in admin and other displays
     def __str__(self):
        return self.title
     