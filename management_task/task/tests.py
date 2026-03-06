from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Task, Project

class TaskAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and token for authentication
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)

        # Create a project
        self.project = Project.objects.create(name="Project Alpha", description="Sample Project")

        # Create a task for this user
        self.task = Task.objects.create(
            title="User Task",
            description="Belongs to testuser",
            priority=1,
            project=self.project,
            user=self.user
        )

        # API URLs
        self.list_url = reverse('task-list')  # /task/
        self.detail_url = lambda pk: reverse('task-list') + f"{pk}/"  # /task/<id>/

    def authenticate(self, email='test@example.com', password='password123'):
        """Helper to authenticate the user with email & password"""
        login = self.client.login(username=email, password=password)  # Django login requires username
        if login:
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return login

    # ---------- TESTS ----------

    def test_login_with_correct_credentials(self):
        is_logged_in = self.authenticate()
        self.assertTrue(is_logged_in)

    def test_login_with_wrong_credentials(self):
        is_logged_in = self.authenticate(email='wrong@example.com', password='wrongpass')
        self.assertFalse(is_logged_in)

    def test_list_tasks_authenticated(self):
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.task.title)

    def test_list_tasks_unauthenticated(self):
        # Without login, access should fail
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_authenticated(self):
        self.authenticate()
        data = {
            "title": "New Task",
            "description": "Test task creation",
            "priority": 2,
            "project_id": self.project.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Task")
        self.assertEqual(Task.objects.get(id=response.data['id']).user, self.user)

    def test_create_task_unauthenticated(self):
        data = {
            "title": "Unauthorized Task",
            "description": "Should not create",
            "priority": 3,
            "project_id": self.project.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task_authenticated(self):
        self.authenticate()
        data = {"title": "Updated Task"}
        response = self.client.patch(self.detail_url(self.task.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task_authenticated(self):
        self.authenticate()
        response = self.client.delete(self.detail_url(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        