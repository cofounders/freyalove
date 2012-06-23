from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, AnonymousUser

from freyalove.matchmaker.models import Match
from freyalove.users.models import Profile

class MatchMakingTest(TestCase):
    def setUp(self):
        # We start off with 2 valid profiles
        self.profile_alpha = Profile()
        self.profile_alpha.first_name = "Test"
        self.profile_alpha.last_name = "User"
        self.profile_alpha.age = "29"
        self.profile_alpha.save()

        self.profile_beta = Profile()
        self.profile_beta.first_name = "Test2"
        self.profile_beta.last_name = "User2"
        self.profile_beta.age = "44"
        self.profile_beta.save()

        self.profile_charlie = Profile()
        self.profile_charlie.first_name = "Match"
        self.profile_charlie.last_name = "Maker"
        self.profile_charlie.age = "31"
        self.profile_charlie.save()

    def test_profiles_are_valid_for_matchmaking(self):
        """
        Test that profiles are valid (not banned or any such flags/state/moderation) before a matchmaking can take place.
        """
        
        self.profile_alpha.banned = True
        self.profile_alpha.save()

        self.match = Match()
        self.match.matchmaker = self.profile_charlie
        self.match.p1 = self.profile_alpha
        self.match.p2 = self.profile_beta

        try:
            self.match.save()
        except ValidationError as v:
            assert v.messages[0] == "Invalid profile in attempt to matchmake!"

    def test_flags_are_properly_assigned_on_responses(self):
        self.match = Match()
        self.match.matchmaker = self.profile_charlie
        self.match.p1 = self.profile_alpha
        self.match.p2 = self.profile_beta

        # Test reject flag
        self.match.save()
        self.match.p1_response = "Declined"
        self.match.save()

        assert self.match.rejected == True

        # Test rejected flag
        self.match.delete()
        self.match = Match()
        self.match.matchmaker = self.profile_charlie
        self.match.p1 = self.profile_alpha
        self.match.p2 = self.profile_beta

        # Test success flag
        self.match.save()
        self.match.p1_response = "Accepted"
        self.match.p2_response = "Accepted"
        self.match.save()

        assert self.match.success == True

    def test_match_save_fails_when_invalid_response(self):
        self.match = Match()
        self.match.matchmaker = self.profile_charlie
        self.match.p1 = self.profile_alpha
        self.match.p2 = self.profile_beta

        self.match.p1_response = "Invalid p1_response"

        try:
            self.match.save()
        except ValidationError as v:
            assert v.messages[0] == "Invalid response in attempt to matchmake!"

    def tearDown(self):
        self.profile_alpha.delete()
        self.profile_beta.delete()
        self.profile_charlie.delete()