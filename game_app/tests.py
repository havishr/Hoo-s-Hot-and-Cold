from django.test import TestCase
from django.urls import reverse
from oauth_app.models import AppUser

from game_app.models import Game
from game_app.forms import GameForm


# Create your tests here.

def create_game(name, approved, latitude=0, longitude=0):
    """
    Creates a specific game instance
    """
    return Game.objects.create(name=name, is_approved=approved,
                               latitude=latitude, longitude=longitude
                               )


class ApproveViewTests(TestCase):
    # Sets up the two user types for testing
    # From: ChatGPT
    def setUp(self):
        # Create a custom user with is_special_user set to True
        self.admin_user = AppUser.objects.create_user(
            username='admin',
            password='admin',
            is_admin=True,
        )

        # Create a custom user with is_special_user set to False
        self.regular_user = AppUser.objects.create_user(
            username='regular',
            password='regular',
            is_admin=False,
        )

    # From: Django tutorial
    def test_no_permissions(self):
        """
        If logged in as regular user, display admin log in requirement.
        """
        # Regular user logged in
        self.client.force_login(self.regular_user)

        response = self.client.get(reverse("approval"))
        self.assertEqual(response.status_code, 403)

    def test_permissions(self):
        """
        If logged in as regular user, display admin log in requirement.
        """
        # Admin user logged in
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse("approval"))
        self.assertEqual(response.status_code, 200)

    # From: Django tutorial
    def test_no_games_submitted(self):
        """
        If no games exist, an appropriate message is displayed.
        """
        # Admin user logged in
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse("approval"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No games awaiting approval...")
        self.assertQuerySetEqual(response.context["game_submissions"], [])

    # From: Django tutorial
    def test_all_games_approved(self):
        """
        Tests that no games are displayed if all games have been approved.
        """
        # Admin user logged in
        self.client.force_login(self.admin_user)

        create_game(name="Rotunda", approved=True)
        create_game(name="Scott Stadium", approved=True)
        response = self.client.get(reverse("approval"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No games awaiting approval...")
        self.assertQuerySetEqual(response.context["game_submissions"], [])

    # From: Django tutorial
    def test_game_not_approved(self):
        """
        Tests that games are displayed if they have not been approved.
        """
        # Admin user logged in
        self.client.force_login(self.admin_user)

        create_game(name="Rotunda", approved=True)
        game = create_game(name="Scott Stadium", approved=False)
        response = self.client.get(reverse("approval"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["game_submissions"], [game])

#From ChatGPT and Online Tutorial
class GameFormTests(TestCase):
    def test_valid_form(self):
        """
        Test that the GameForm is valid with correct data.
        """
        data = {
            'name': 'New Game',
            'latitude': 38.0353,
            'longitude': -78.5035
        }
        form = GameForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test that the GameForm is invalid with incorrect data.
        """
        data = {
            'name': '',
            'latitude': 'invalid_latitude',
            'longitude': 'invalid_longitude'
        }
        form = GameForm(data)
        self.assertFalse(form.is_valid())

class TemplateTests(TestCase):
    def setUp(self):
        self.admin_user = AppUser.objects.create_user(username='admin', password='admin', is_admin=True)
        self.client.force_login(self.admin_user)
        self.game = create_game(name="Test Game", approved=False)

    def test_approval_template_display(self):
        """
        Test that the approval template displays games awaiting approval.
        """
        response = self.client.get(reverse("approval"))
        self.assertContains(response, "Test Game")
        self.assertContains(response, "Approve")
        self.assertContains(response, "Deny")

    def test_addgame_template_display(self):
        """
        Test that the addgame template displays the form correctly.
        """
        response = self.client.get(reverse("add_game"))
        self.assertContains(response, "Create Game")
        self.assertContains(response, "name")
        self.assertContains(response, "latitude")
        self.assertContains(response, "longitude")