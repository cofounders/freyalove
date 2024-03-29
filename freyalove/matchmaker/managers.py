from django.db import models

import datetime

class MatchManager(models.Manager):
    def has_match(self, profile):
        matches = super(MatchManager, self).get_query_set().filter(p1=profile)
        if matches.count() == 0:
            matches = super(MatchManager, self).get_query_set().filter(p2=profile)
            if matches.count() == 0:
                return False
            else:
                return True
        else:
            return True

    def all_matches(self, profile):
        matches_1 = list(super(MatchManager, self).get_query_set().filter(p1=profile))
        matches_2 = list(super(MatchManager, self).get_query_set().filter(p2=profile))

        return matches_1 + matches_2

class MatchProposalManager(models.Manager):
    def fetch_match_proposals(self, profile):
        profiles = []
        mp_1 = super(MatchProposalManager, self).get_query_set().filter(from_profile=profile).order_by('quality')
        mp_2 = super(MatchProposalManager, self).get_query_set().filter(to_profile=profile).order_by('quality')

        for mp in mp_1:
            profiles.append(mp.to_profile)

        for mp in mp_2:
            profiles.append(mp.from_profile)

        return profiles

    def get_match_proposal(self, profile1, profile2):
        mp = super(MatchProposalManager, self).get_query_set().filter(from_profile=profile1, to_profile=profile2)
        if mp.count() > 0:
            pass
        else:
            mp = super(MatchProposalManager, self).get_query_set().filter(from_profile=profile2, to_profile=profile1)

        return mp
        

class SexyTimeManager(models.Manager):
    def fetch_sexytimes(self, profile):
        now = datetime.datetime.now()
        sexytimes_1 = super(SexyTimeManager, self).get_query_set().filter(p1=profile).filter(rejected=False)
        sexytimes_2 = super(SexyTimeManager, self).get_query_set().filter(p2=profile).filter(rejected=False)

        return list(sexytimes_1) + list(sexytimes_2)