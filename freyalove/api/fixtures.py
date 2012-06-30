# Dump some test data/or remove?

# GLOBAL IMPORTS
import os, sys, time
from os.path import abspath, dirname, join

CURRENT_DIR = dirname(__file__)
sys.path.insert(0, abspath(join(CURRENT_DIR, '..')))

from django.core.management import setup_environ
import settings

setup_environ(settings)

# DJANGO IMPORTS AFTER THIS LINE
from freyalove.users.models import Profile

print "Current users count: %d" % Profile.objects.all().count()


# Let's add some users
def create_profile(profile_instance):
	try:
		existing_profile = Profile.objects.get(fb_id=profile_instance.fb_id)
		return existing_profile
	except Profile.DoesNotExist:
		profile_instance.save()
		print "Created profile: %d" % profile_instance.id
		return profile_instance

"""
p = Profile()
p.fb_id = "10151211264108098"
p.first_name = "Kenny"
p.last_name = "Shen"
p.fb_username = "kennyshen"
create_profile(p)
"""

# DESTROY!
p = Profile.objects.all()
for x in p:
	x.delete()
