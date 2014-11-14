import requests
# Get the token using a POST request and a code

# import settings
from django.conf import settings


OAUTH_KEY = "access_token"
CODE_KEY = "code" 
GENOME_KEY = "genome"
NEANDERTHAL_KEY = "neanderthal"
PROFILE_KEY = "profiles"

class For23andMe(object):
    '''
    This class encapsulates how to create requests to the 23andMe server. 
    '''

    def __init__(self, access_token=None):
        self._BASE_URL = "https://api.23andme.com/1"
        self._scope = '''basic names rs53576 rs1815739 rs6152 rs1800497 rs1805007 rs9939609
            rs662799 rs7495174 rs7903146 rs12255372 rs1799971
            rs17822931 rs4680 rs1333049 rs1801133 rs1051730 rs3750344
            rs4988235'''
        self._scope = 'basic names genomes'
        self._demo = True
        self._LILY = 'SP1_MOTHER_V4'
        self._GREG = 'SP1_FATHER_V4'
        self.access_token = access_token

    def authorize(self):
        login_url = "https://api.23andme.com/authorize/"
        login_url += "?redirect_uri=%s" % settings.CALLBACK_URL
        login_url += "&response_type=code&client_id=%s&scope=%s" % (settings.CLIENT_ID, self._scope)
        return login_url

    def get_scope(self):
        return self._scope
        
    def set_scope(self, scope):
        self._scope = scope

    def get_token(self, authorization_code):
        parameters = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': authorization_code, # the authorization code obtained above
            'redirect_uri': settings.CALLBACK_URL,
            'scope': self._scope,
        }
        response = requests.post(
            "https://api.23andme.com/token/",
            data = parameters
        )

        print ("response.json: {0}".format(response.json()))
        if response.status_code == 200:
            return (response.json()['access_token'], response.json()['refresh_token'])
        else:
            response.raise_for_status()

    def refresh_token(self, refresh_token):
        parameters = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'redirect_uri': settings.CALLBACK_URL,
            'scope': self._scope,
        }
        response = requests.post(
            "https://api.23andme.com/token/",
            data = parameters
        )

        print ( "response.json: {0}".format(response.json()))
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return (response.json()['access_token'], response.json()['refresh_token'])
        else:
            response.raise_for_status()

    def _get_resource(self, resource):
        '''Given a uri, return a tuple consisting of status and dictionary. Or
        raised an exception. 
        '''
        if self.access_token is None:
            raise Exception("access_token cannot be None")

        headers = {'Authorization': 'Bearer %s' % self.access_token}
        url = "%s%s" % (self._BASE_URL, resource)
        response = requests.get(
            url,
            headers=headers,
            verify=False,
        )
        print ( "url: {0}".format(url) )
        print ( "response: {0}".format(response) )
        # print ( "response.json: {0}".format(response.json()) )
        # print ( "response.text: {0}".format(response.text) )
        
        if response.status_code == 200:
            return (200, response.text)
        elif response.status_code == 403:
            return (403, {'error' : '/forbidden/'})  # suppose custome 403 page
        else:
            response.raise_for_status()

    # User info 
    def get_user_request(self, demo=True):
        uri = '/demo/' if demo else '/'
        uri += 'user/?services=true'
        return self._get_resource(uri)

    def get_names_request(self, demo=False):
        uri = '/demo/' if demo else '/'
        uri += 'names/'
        return self._get_resource(uri)

    # Genetics
    def get_genome_request(self, profile_id, unfiltered=False, demo=False):
        uri = '/demo/' if self._demo else '/'
        uri += 'genomes/' + profile_id
        # if unfiltered:
        #     uri += '?unfiltered=True'
        # else:
        #     uri += '?unfiltered=False'
        return self._get_resource(uri)

    def get_genotype_request(self, profile_id, locations, unfiltered=False, demo=False):
        uri = '/demo/' if demo else '/'
        uri += 'genotypes/' + profile_id
        uri += '?locations=%s' % locations
        if unfiltered:
            uri += '?unfiltered=True'
        else:
            uri += '?unfiltered=False'
        return self._get_resource(uri)

    # Ancestry
    def get_neanderthal_request(self, profile_id=None, demo=False):
        if self._demo:
            uri = '/demo/'
            uri += 'neanderthal/'
            uri += self._LILY
        else:
            uri = '/'
            uri += 'neanderthal/'
            uri += profile_id

        return self._get_resource( uri )
