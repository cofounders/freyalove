from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def homepage(request):
	"""
	Show me the homepage!
	"""
	template = "home.html"

	resp = render_to_response(template, {
    }, context_instance=RequestContext(request))

    return resp