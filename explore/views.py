from django.http import HttpResponse
from django.shortcuts import redirect, render

import json
import logging

log = logging.getLogger("curio.explore")

from . import client

# user info
def names_request(request):
    page = "home.html"
    c = client.For23andMe(request.session[client.OAUTH_KEY])
    (status, context) =  c.get_names_request() 
    return render(request, page)

def user_request(request):

    c = client.For23andMe(request.session[client.OAUTH_KEY])
    (status, context) = c.get_user_request()
    page = "home.html"
    if status == 403: 
        page = "forbidden.html"
    return render (request, page)

# Ancestry
def neanderthal_request(request):
    c = client.For23andMe(request.session[client.OAUTH_KEY])
    (status, context) = c.get_neanderthal_request() 
    page = "home.html"
    if status == 403: 
        page = "forbidden.html"
    return render( request, page )

# Genetics 
def genome_request(request):
    c = client.For23andMe(request.session[client.OAUTH_KEY])
    (status, context) = c.get_genome_request() 
    page = "home.html"
    if status == 403: 
        page = "forbidden.html"
    return HttpResponse( request, page )

def genotype_request(request, snpid):
    c = client.For23andMe(request.session[client.OAUTH_KEY])
    (status, context) =  c.get_genotype_request(snpid) 
    page = "home.html"
    if status == 403: 
        page = "forbidden.html"
    return HttpResponse(request, page )

"""
The 23andMe api calls this view with a ?code=xxxxxx paramter. This
parameter is a short lived authorization code that you must use to get
a an OAuth authorization token which you can use to retrieve user
data. This view uses database backed session to store the auth token
instead of cookies in order to protect the token from leaving the
server as it allows access to significant sensitive user information.
"""
def callback(request):
    import pdb; pdb.set_trace()
    if client.CODE_KEY in request.GET:
        c = client.For23andMe()
        code = request.GET[client.CODE_KEY]
        log.debug("code: %s" % code)
        
        log.debug("fetching token...")

        (access_token, refresh_token) = c.get_token(code)
        log.debug("access_token: %s refresh_token: %s" % (access_token, refresh_token))

        log.debug("refreshing token...")

        (access_token, refresh_token) = c.refresh_token(refresh_token)
        log.debug("access_token: %s refresh_token: %s" % (access_token, refresh_token))

        request.session[client.OAUTH_KEY] = access_token

        c = client.For23andMe(request.session[client.OAUTH_KEY])
        names_json = c.get_names()
        names = json.loads(names_json)
        request.session["name"] = "%s %s" % (names['first_name'], names['last_name'])
    elif client.GENOME_KEY in request.GET:
        with open("/home/jkern/data/genomic/23andme/lily_mendel.txt", "w") as outport:
            output.write(request.GET[client.GENOME_KEY])
    elif client.NEANDERTHAL_KEY in request.GET:
        print(json.dumps(request.GET[client.NEANDERTHAL_KEY]))
    elif client.PROFILE_KEY in request.GET:
        import pdb; pdb.set_trace()
    return redirect("/home/")


def logout(request):
    log.debug("logging out...")
    request.session.clear()
    return redirect("/")

def home(request):
    # FIXME check session for OAuth token
    if client.OAUTH_KEY in list(request.session.keys()):
        access_token = request.session[client.OAUTH_KEY]
        log.debug("user has oauth access token: %s" % access_token)
        return render(request, 'home.html', { 'user_name': request.session['name']})
    else:
        log.debug("user doesn't have a token yet, redirect to login...")
        return redirect( client.For23andMe().authorize() )

