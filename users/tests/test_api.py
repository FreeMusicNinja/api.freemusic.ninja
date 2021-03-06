from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class UserTest(APITestCase):

    """Tests for /users/ API endpoints."""

    def test_list_users_logged_out(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == [{
            'id': 1,
            'name': "",
        }])

    def test_view_user_logged_out(self):
        user = User.objects.create(name="Trey", email="trey@example.com")
        url = reverse('user-detail', args=[user.pk])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == {
            'id': user.id,
            'name': user.name,
        })

    def test_same_user(self):
        user = User.objects.create(name="Trey", email="trey@example.com")
        url = reverse('user-detail', args=[user.pk])
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        })

    def test_different_user(self):
        user1 = User.objects.create(name="User1", email="user1@example.com")
        user2 = User.objects.create(name="User2", email="user2@example.com")
        url = reverse('user-detail', args=[user1.pk])
        self.client.force_authenticate(user=user2)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == {
            'id': user1.id,
            'name': user1.name,
        })

    def test_me_logged_out(self):
        url = reverse('user-detail', args=['me'])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_me_logged_in(self):
        user = User.objects.create(name="Trey", email="trey@example.com")
        url = reverse('user-detail', args=['me'])
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        })

    def test_update_current_user(self):
        user = User.objects.create(name="Trey", email="trey@example.com")
        self.check_update(user.pk, user)

    def test_update_me(self):
        user = User.objects.create(name="Trey", email="trey@example.com")
        self.check_update('me', user)

    def check_update(self, pk, user):
        new_name = "Bob"
        new_email = "bob@example.com"
        url = reverse('user-detail', args=[pk])
        self.client.force_authenticate(user=user)
        response = self.client.put(url, format='json', data={
            'name': new_name,
            'email': new_email,
        })
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == {
            'id': user.id,
            'name': new_name,
            'email': new_email,
        })
