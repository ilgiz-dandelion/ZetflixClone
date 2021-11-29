from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import MyUser
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "email": "testcase@example.com",
            "password": "NewPassword@123",
            "password_confirm": "NewPassword@123"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='ilgiz@gmail.com', password='1')
        self.token = Token.objects.create(user=self.user)
        self.user.is_active = True


    def test_login(self):
        data = {
            'email': 'ilgiz@gmail.com', 'password': '1'
        }
        response = self.client.post(reverse('login'), data)
        return(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.is_active = True

    def test_logout(self):
        self.token = Token.objects.get(user__email="ilgiz@gmail.com")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        return(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)