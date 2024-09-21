from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Task, UserResponse

User = get_user_model()

class SendEmailViewTest(APITestCase):

    def test_send_email_with_valid_data(self):
        url = reverse('send-email')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Email will be sent shortly.")

    def test_send_email_with_invalid_data(self):
        url = reverse('send-email')
        data = {'email': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Email is required.")


class TaskCreateViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_task_success(self):
        url = reverse('task-create')
        data = {'title': 'New Task', 'description': 'Task description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'New Task')
        self.assertEqual(Task.objects.first().user, self.user)

    def test_create_task_unauthenticated(self):
        self.client.logout()
        url = reverse('task-create')
        data = {'title': 'New Task', 'description': 'Task description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskListViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.client.force_authenticate(user=self.user)
        Task.objects.create(title='Task 1', description='First task', user=self.user)
        Task.objects.create(title='Task 2', description='Second task', user=self.user)

    def test_list_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Task 1')
        self.assertEqual(response.data[1]['title'], 'Task 2')

    def test_list_tasks_unauthenticated(self):
        self.client.logout()
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskDetailViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(title='Task Detail', description='Detail task', user=self.user)

    def test_task_detail_success(self):
        url = reverse('task-detail', kwargs={'id': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task Detail')

    def test_task_detail_not_found(self):
        url = reverse('task-detail', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_detail_unauthenticated(self):
        self.client.logout()
        url = reverse('task-detail', kwargs={'id': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserResponseCreateViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_user_response_success(self):
        url = reverse('user-response-create')
        data = {
            'experience': 'Amazing',
            'huddle_feedback': 'Great platform!',
            'feature_suggestion': 'Add video conferencing.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserResponse.objects.count(), 1)
        self.assertEqual(UserResponse.objects.first().experience, 'Amazing')
        self.assertEqual(UserResponse.objects.first().user, self.user)

    def test_create_user_response_unauthenticated(self):
        self.client.logout()
        url = reverse('user-response-create')
        data = {
            'experience': 'Amazing',
            'huddle_feedback': 'Great platform!',
            'feature_suggestion': 'Add video conferencing.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
