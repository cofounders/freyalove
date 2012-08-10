from freyalove.notifications.models import Notification

def register_wink(sender, instance, **kwargs):
	try:
		n = Notification.objects.get(wink=instance)
		if instance.accepted and instance.received:
			n.status = "1"
			n.marked_for_removal = True
		elif instance.received and not instance.accepted:
			n.status = "2"
			n.marked_for_removal = True
		else:
			pass
		n.save()
	except Notification.DoesNotExist:
		n = Notification()
		n.profile = instance.to_profile
		n.ntype = "1"
		n.status = "2"
		n.wink = instance
		n.save()

