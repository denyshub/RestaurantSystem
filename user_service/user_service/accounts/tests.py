from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress, EmailConfirmationHMAC

User = get_user_model()


class AuthTestCase(APITestCase):
    def setUp(self):
        self.register_url = "/auth/registration/"
        self.login_url = "/auth/login/"
        self.user_data = {
            "email": "testuser@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "username": "Test User",
        }

    def test_registration_start(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.filter(email=self.user_data["email"]).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)

        email_address = EmailAddress.objects.get(user=user)
        self.assertFalse(email_address.verified)

    def test_login_not_verified(self):
        # Створюємо користувача
        response = self.client.post(
            self.register_url,
            {
                "email": "login@example.com",
                "password1": "TestPass123!",
                "password2": "TestPass123!",
                "username": "Test User",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_data = {"email": "login@example.com", "password": "TestPass123!"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("E-mail is not verified.", str(response.data))

    def test_verify_email_and_login(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=self.user_data["email"])
        email_address = EmailAddress.objects.get(user=user, email=user.email)

        self.assertFalse(email_address.verified)

        email_address.verified = True
        email_address.save()

        email_address.refresh_from_db()
        self.assertTrue(email_address.verified)

        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password1"],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login(self):
        user = User.objects.create_user(
            email="login@example.com",
            password="TestPass123!",
            full_name="Test User",
            is_active=True,
        )
        EmailAddress.objects.create(
            user=user, email=user.email, verified=True, primary=True
        )

        login_data = {"email": "login@example.com", "password": "TestPass123!"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        user = User.objects.create_user(
            email="refresh@example.com",
            password="TestPass123!",
            full_name="Test User",
            is_active=True,
        )
        EmailAddress.objects.create(
            user=user, email=user.email, verified=True, primary=True
        )

        login_data = {"email": "refresh@example.com", "password": "TestPass123!"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 200)

        refresh_token = response.data["refresh"]
        refresh_response = self.client.post(
            "/auth/token/refresh/", {"refresh": refresh_token}
        )
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn("access", refresh_response.data)

    def test_login_wrong_password(self):
        user = User.objects.create_user(
            email="fail@example.com", password="CorrectPass123!", full_name="Test User"
        )
        EmailAddress.objects.create(
            user=user, email=user.email, verified=True, primary=True
        )

        response = self.client.post(
            self.login_url, {"email": "fail@example.com", "password": "WrongPassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
