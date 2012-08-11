from django.db import models

class ProfileManager(models.Manager):

    def has_freya_profile_given_fb_details(self, fb_val):
        try:
            fb_id = int(fb_val)
        except ValueError:
            fb_id = None

        if not fb_id:
            try:
                profile = self.get(fb_username=fb_val)
            except self.model.DoesNotExist:
                pass
        else:
            try:
                profile = Profile.objects.get(fb_id=val)
            except self.model.DoesNotExist:
                pass

        return profile

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

class WinkManager(models.Manager):

    def has_wink_for_profiles(self, profile1, profile2):
        has_wink = False
        p1_to_p2 = self.filter(to_profile=profile1, from_profile=profile2)
        if p1_to_p2.count() > 0:
            for w in p1_to_p2:
                if w.received and w.accepted:
                    has_wink = True

        if not has_wink:
            p2_to_p1 = self.filter(to_profile=profile2, from_profile=profile1)
            if p2_to_p1.count() > 0:
                for w in p2_to_p1:
                    if w.received and w.accepted:
                        has_wink = True
        return has_wink