from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from django.contrib import auth

from .forms import RegistrationForm, LoginForm


def create_user(username, password, email="default@default.com"):
    User.objects.create_user(username, email, password)


class RegistrationFormTests(TestCase):
    def test_enter_correct_registration_infos(self):
        """
        On correct entry the form is valid
        """
        form_data = {'username': 'testuser', 'password': '12345',
            'password_confirm': '12345', 'email': 'test@test.com'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_enter_correct_registration_infos_without_email(self):
        """
        Form entry without email
        """
        form_data = {'username': 'testuser', 'password': '12345',
            'password_confirm': '12345'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_not_match(self):
        """
        Returns error if the passwords not match
        """
        form_data = {'username': 'testuser', 'password': '12345',
            'password_confirm': '123456'}
        form = RegistrationForm(data=form_data)
        self.assertRaises(forms.ValidationError)

    def test_empty_username_field(self):
        """
        Returns error if username empty
        """
        form_data = {'password': '12345', 'password_confirm': '12345'}
        form = RegistrationForm(data=form_data)
        self.assertRaises(forms.ValidationError)

    def test_blank_username_field(self):
        """
        Returns error if username blank
        """
        form_data = {'username': ' ', 'password': '12345', 'password_confirm': '12345'}
        form = RegistrationForm(data=form_data)
        self.assertRaises(forms.ValidationError)

    def test_incorrect_email(self):
        form_data = {'username': 'testuser', 'password': '12345', 'password_confirm': '12345',
            'email' : 'aaa@aaa'}
        form = RegistrationForm(data=form_data)
        self.assertRaises(forms.ValidationError)


class LoginFormTests(TestCase):
    def test_valid_entry(self):
        form_data = {'username': 'testuser', 'password': '12345'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_username_field(self):
        form_data = {'password': '12345'}
        form = LoginForm(data=form_data)
        self.assertRaises(forms.ValidationError)

    def test_empty_password_field(self):
        form_data = {'username': 'testuser'}
        form = LoginForm(data=form_data)
        self.assertRaises(forms.ValidationError)


class RegistrationViewTests(TestCase):
    def test_redirect_on_successful_registration(self):
        """
        Redirects to success page on successful registration
        """
        post_data = {'username': 'testuser', 'password': '12345',
            'password_confirm': '12345'}
        response = self.client.post(reverse('users:registration'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:registration success'))

    def test_create_user_on_successful_registration(self):
        """
        Creates the new user on successful registration with default email address
        """
        post_data = {'username': 'testuser', 'password': '12345',
            'password_confirm': '12345'}
        self.client.post(reverse('users:registration'), post_data)

        user = User.objects.get(username='testuser')
        self.assertTrue(user.check_password('12345'))
        self.assertEqual(user.email, "default@default.com")

    def test_registration_failure_identical_usernames(self):
        """
        Failure when creating two users with identical usernames
        """
        post_data = {'username': 'testuser', 'password': '12345',
            'password_confirm': '12345'}
        self.client.post(reverse('users:registration'), post_data)
        response = self.client.post(reverse('users:registration'), post_data)

        self.assertEqual(response.status_code, 200)

        list_of_error_list = list(response.context['form'].errors.values())
        error_list = []

        for one_list in list_of_error_list:
            for error in one_list:
                error_list.append(error)

        self.assertIn("Registration failed!", error_list)


class LoginViewTests(TestCase):
    def test_redirect_on_valid_entry(self):
        create_user("testuser", "12345")
        post_data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('users:login'), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('posts:index'))

    def test_logged_in_on_valid_entry(self):
        create_user("testuser", "12345")
        post_data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('users:login'), post_data)

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, "testuser")

    def test_on_login_failure(self):
        """
        On login failure the login form shows error message and no use is logged in
        """
        post_data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('users:login'), post_data)

        self.assertEqual(response.status_code, 200)

        list_of_error_list = list(response.context['form'].errors.values())
        error_list = []

        for one_list in list_of_error_list:
            for error in one_list:
                error_list.append(error)

        self.assertIn("Login failed!", error_list)

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
