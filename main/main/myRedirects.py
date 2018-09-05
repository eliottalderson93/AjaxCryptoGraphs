from django.http import HttpResponsePermanentRedirect
def home(req):
    print("redirect")
    return HttpResponsePermanentRedirect("/home/")