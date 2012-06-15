from django.db import models

class FriendshipManager(models.Manager):

    def friends_for_profile(self, profile):
        friends = []
        for friendship in self.filter(from_profile=profile).select_related(depth=1):
            friends.append({"friend": friendship.to_profile, "friendship": friendship})
        for friendship in self.filter(to_profile=profile).select_related(depth=1):
            friends.append({"friend": friendship.to_profile, "friendship": friendship})
        return friends

    def are_friends(self, profile1, profile2):
        if self.filter(from_profile=profile1, to_profile=profile2).count() > 0:
            return True
        if self.filter(from_profile=profile2, to_profile=profile1).count() > 0:
            return True
        return False

    def unfriend(self, profile1, profile2):
        if self.filter(from_profile=profile1, to_profile=profile2):
            friendship = self.filter(from_profile=profile1, to_profile=profile2)
        elif self.filter(from_profile=profile2, to_profile=profile1):
            friendship = self.filter(from_profile=profile2, to_profile=profile1)
        friendship.delete()