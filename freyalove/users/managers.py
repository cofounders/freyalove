from django.db import models
from django.utils import timezone

import datetime
import facebook

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
            #friends.append({"friend": friendship.to_profile, "friendship": friendship})
            friends.append(friendship.to_profile)
        for friendship in self.filter(to_profile=profile).select_related(depth=1):
            #friends.append({"friend": friendship.from_profile, "friendship": friendship})
            friends.append(friendship.from_profile)
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

class FriendsCacheManager(models.Manager):

    def update_cache(self, profile, token):
        cache = super(FriendsCacheManager, self).get_query_set().get(profile=profile)
        # check to see if to be updated
        if timezone.make_aware((cache.updated + datetime.timedelta(hours=2)), timezone.get_default_timezone()) < timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()): 
            graph = facebook.GraphAPI(token)
            friends = graph.get_connections("me", "friends")
            friends = friends["data"]
            friends_ids = []
            for entry in friends:
                friends_ids.append(entry["id"])

            friends_as_str = ",".join(friends_ids)
            cache.fb_ids = friends_as_str
            cache.updated = datetime.datetime.now()
            cache.save()

            # update friendships in the system
            from freyalove.users.models import Profile, Friendship
            other_profiles = Profile.objects.filter(fb_id__in=friends_ids)
            for p in other_profiles:
                if Friendship.are_friends(profile, p):
                    pass
                else:
                    f = Friendship()
                    f.to_profile = p
                    f.from_profile = profile
                    f.save()