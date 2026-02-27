from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from task.models import Task

class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")

        # Create a sample task for user1
        self.task1 = Task.objects.create(
            user=self.user1,
            title="Test Task 1",
            description="Some description",
            due_date=timezone.now() + timezone.timedelta(days=7),
            priority_level='LOW',
            status='PENDING'
        )

    # Test creating a task
    def test_create_task(self):
        self.client.login(username="user1", password="pass123")
        data = {
            "title": "New Task",
            "description": "Task description",
            "due_date": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "priority_level": "MEDIUM",
            "status": "PENDING"
        }
        response = self.client.post("/tasks/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    # Test listing tasks as authenticated user
    def test_list_tasks_authenticated(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test listing tasks as unauthenticated user
    def test_list_tasks_unauthenticated(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test updating a task owned by the user
    def test_update_task(self):
        self.client.login(username="user1", password="pass123")
        data = {"status": "IN_PROGRESS"}
        response = self.client.patch(f"/tasks/{self.task1.id}/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, "IN_PROGRESS")

    # Test updating a task not owned by the user
    def test_update_task_not_owned(self):
        self.client.login(username="user2", password="pass123")
        data = {"status": "COMPLETED"}
        response = self.client.patch(f"/tasks/{self.task1.id}/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test deleting a task owned by the user
    def test_delete_task(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.delete(f"/tasks/{self.task1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    # Test deleting a task not owned by the user
    def test_delete_task_not_owned(self):
        self.client.login(username="user2", password="pass123")
        response = self.client.delete(f"/tasks/{self.task1.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.count(), 1)
        