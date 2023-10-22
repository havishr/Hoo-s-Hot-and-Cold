from django.test import TestCase
from django.urls import reverse
from oauth_app.models import AppUser

from game_app.models import Game


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

# class ApproveGameTest(TestCase):
#     def test_approve_game(self):
#         """
#         Tests that a game's is_approved field is set to True when approved
#         """
#         game = create_game(name="Rotunda", approved=False)
