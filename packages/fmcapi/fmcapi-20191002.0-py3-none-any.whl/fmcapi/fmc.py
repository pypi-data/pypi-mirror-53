"""
This module (fmc.py) is designed to provide a "toolbox" of tools for interacting with the Cisco FMC API.
The "toolbox" is the FMC class and the "tools" are its methods.

Note: There exists a "Quick Start Guide" for the Cisco FMC API too.  Just Google for it as it gets updated with each
 release of code.
"""

import datetime
import requests
import time
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from logging.handlers import RotatingFileHandler
import warnings

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

""""
The 'requests' package is very chatty on the INFO logging level.  Change its logging threshold sent to logger to 
something greater than INFO (i.e. not INFO or DEBUG) will cause it to not log its INFO and DEBUG messages to the 
default logger.  This reduces the size of our log files.
"""
logging.getLogger("requests").setLevel(logging.WARNING)


# noinspection SpellCheckingInspection
class FMC(object):
    """
The FMC class has a series of methods, lines that start with "def", that are used to interact with the Cisco FMC
via its API.  Each method has its own DOCSTRING (like this triple quoted text here) describing its functionality.
    """
    logging.debug("In the FMC() class.")

    API_CONFIG_VERSION = 'api/fmc_config/v1'
    API_PLATFORM_VERSION = 'api/fmc_platform/v1'
    VERIFY_CERT = False
    MAX_PAGING_REQUESTS = 2000
    TOO_MANY_CONNECTIONS_TIMEOUT = 30
    FMC_MAX_PAYLOAD = 2048000

    def __init__(self,
                 host='192.168.45.45',
                 username='admin',
                 password='Admin123',
                 domain=None,
                 autodeploy=True,
                 file_logging=None,
                 logging_level='INFO',
                 debug=False,
                 limit=1000):
        """
        Instantiate some variables prior to calling the __enter__() method.
        :param host:
        :param username:
        :param password:
        :param autodeploy:
        :param file_logging (str): The filename (and optional path) of the output file if a file logger is required,
        None if no file logger is required
        :param logging_level (str): The desired logging level, INFO by default.
        :param debug (bool): True to enable debug logging, default is False
        :param limit (int): Sets up max page of data to gather per "page".
        """

        if debug:
            logging_level = 'DEBUG'
        root_logger = logging.getLogger('')
        if logging_level.upper() == 'DEBUG':
            root_logger.setLevel(logging.DEBUG)
        if logging_level.upper() == 'INFO':
            root_logger.setLevel(logging.INFO)
        if logging_level.upper() == 'WARNING':
            root_logger.setLevel(logging.WARNING)
        if logging_level.upper() == 'ERROR':
            root_logger.setLevel(logging.ERROR)
        if logging_level.upper() == 'CRITICAL':
            root_logger.setLevel(logging.CRITICAL)

        if file_logging:
            print(f'Logging is enabled and set to {logging_level}.  Look for file "{file_logging}" for output.')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(filename)s:%(lineno)s - %(message)s',
                                          '%Y/%m/%d-%H:%M:%S')
            file_logger = RotatingFileHandler(file_logging, maxBytes=1024000, backupCount=10, mode='w')
            file_logger.setFormatter(formatter)
            root_logger.addHandler(file_logger)

        logging.debug("In the FMC __init__() class method.")

        self.host = host
        self.username = username
        self.password = password
        self.domain = domain
        self.autodeploy = autodeploy
        self.limit = limit
        self.vdbVersion = None
        self.sruVersion = None
        self.serverVersion = None
        self.geoVersion = None
        self.configuration_url = None
        self.platform_url = None
        self.page_counter = None

    def __enter__(self):
        """
        Get a token from the FMC as well as the Global UUID.  With this information set up the base_url variable.
        :return:
        """
        logging.debug("In the FMC __enter__() class method.")
        self.mytoken = Token(host=self.host,
                             username=self.username,
                             password=self.password,
                             domain=self.domain,
                             verify_cert=self.VERIFY_CERT)
        self.uuid = self.mytoken.uuid
        self.build_urls()
        self.serverversion()
        logging.info(f"This FMC's version is {self.serverVersion}")
        return self

    def __exit__(self, *args):
        """
        If autodeploy == True push changes to FMC upon exit of "with" contract.
        :param args:
        :return:
        """
        logging.debug("In the FMC __exit__() class method.")

        if self.autodeploy:
            self.deploymentrequests()
        else:
            logging.info("Auto deploy changes set to False.  "
                         "Use the Deploy button in FMC to push changes to FTDs.\n\n")

    def build_urls(self):
        """
        The FMC APIs appear to use 2 base URLs, depending on what that API is for.  One for "configuration" and the
        other for FMC "platform" things.
        """
        logging.debug("In the FMC build_urls() class method.")
        logging.info('Building base to URLs.')
        self.configuration_url = f"https://{self.host}/{self.API_CONFIG_VERSION}/domain/{self.uuid}"
        self.platform_url = f"https://{self.host}/{self.API_PLATFORM_VERSION}"

    def send_to_api(self, method='', url='', headers='', json_data=None, more_items=[]):
        """
        Using the "method" type, send a request to the "url" with the "json_data" as the payload.
        :param method:
        :param url:
        :param headers:
        :param json_data:
        :param more_items:
        :return:
        """
        logging.debug("In the FMC send_to_api() class method.")

        if not more_items:
            self.more_items = []
            self.page_counter = 0
        if headers == '':
            # These values for headers works for most API requests.
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.mytoken.get_token()}
        status_code = 429
        response = None
        json_response = None
        try:
            while status_code == 429:
                if method == 'get':
                    response = requests.get(url, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'post':
                    response = requests.post(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'put':
                    response = requests.put(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'delete':
                    response = requests.delete(url, headers=headers, verify=self.VERIFY_CERT)
                else:
                    logging.error("No request method given.  Returning nothing.")
                    return
                status_code = response.status_code
                if status_code == 429:
                    logging.warning(f"Too many connections to the FMC.  Waiting {self.TOO_MANY_CONNECTIONS_TIMEOUT} "
                                    f"seconds and trying again.")
                    time.sleep(self.TOO_MANY_CONNECTIONS_TIMEOUT)
                if status_code == 401:
                    logging.warning("Token has expired. Trying to refresh.")
                    self.mytoken.access_token = self.mytoken.get_token()
                    headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.mytoken.access_token}
                    status_code = 429
                if status_code == 422:
                    logging.warning("Either:\n\t1. Payload too large.  FMC can only handle a payload of "
                                    f"{self.FMC_MAX_PAYLOAD} bytes.\n\t2.The payload contains an unprocessable or "
                                    f"unreadable entity such as a invalid attribut name or incorrect JSON syntax ")
            json_response = json.loads(response.text)
            if status_code > 301 or 'error' in json_response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(f"Error in POST operation --> {str(err)}")
            logging.error(f"json_response -->\t{json_response}")
            if response:
                response.close()
            return None
        if response:
            response.close()
        try:
            if 'next' in json_response['paging'] and self.page_counter <= self.MAX_PAGING_REQUESTS:
                self.more_items += json_response['items']
                logging.info(f"Paging:  Offset:{json_response['paging']['offset']}, "
                             f"Limit:{json_response['paging']['limit']}, "
                             f"Count:{json_response['paging']['count']}, "
                             f"Gathered_Items:{len(self.more_items)}.")
                self.page_counter += 1
                return self.send_to_api(method=method,
                                        url=json_response['paging']['next'][0],
                                        json_data=json_data,
                                        more_items=self.more_items)
            else:
                json_response['items'] += self.more_items
                self.more_items = []
                return json_response
        except KeyError:
            # Used only when the response only has "one page" of results.
            return json_response

    def serverversion(self):
        """
        Get the FMC's version information.  Set instance variables for each version info returned as well as return
        the whole response text.
        :return:
        """
        logging.debug("In the FMC version() class method.")
        logging.info('Collecting version information from FMC.')

        url_suffix = '/info/serverversion'
        url = f'{self.platform_url}{url_suffix}'

        response = self.send_to_api(method='get', url=url)
        if 'items' in response:
            logging.info('Populating vdbVersion, sruVersion, serverVersion, and geoVersion FMC instance variables.')
            self.vdbVersion = response['items'][0]['vdbVersion']
            self.sruVersion = response['items'][0]['sruVersion']
            self.serverVersion = response['items'][0]['serverVersion']
            self.geoVersion = response['items'][0]['geoVersion']
        return response

    def version(self):
        """Dispose of this method after 20210101."""
        warnings.warn("Deprecated: version() should be called via serverversion().")
        self.serverversion()

    def auditrecords(self):
        """
        This API function supports filtering the GET query URL with: username, subsystem, source, starttime, and
        endtime parameters.
        :return: response
        """
        logging.debug('In the auditrecords method of FMC.')
        url_parameters = 'expanded=true'
        url_suffix = '/audit/auditrecords'
        url = f'{self.platform_url}/domain/{self.uuid}{url_suffix}?{url_parameters}'

        response = self.send_to_api(method='get', url=url)
        return response

    def audit(self):
        """Dispose of this method after 20210101."""
        warnings.warn("Deprecated: audit() should be called via auditrecords().")
        self.auditrecords()

    def deployabledevices(self):
        """
        Collect a list of FMC managed devices who's configuration is not up-to-date.
        :return: List of devices needing updates.
        """
        logging.debug("In the FMC deployabledevices() class method.")

        waittime = 15
        logging.info(f"Waiting {waittime} seconds to allow the FMC to update the list of deployable devices.")
        time.sleep(waittime)
        logging.info("Getting a list of deployable devices.")
        url_suffix = "/deployment/deployabledevices?expanded=true"
        url = f'{self.configuration_url}{url_suffix}'
        response = self.send_to_api(method='get', url=url)
        # Now to parse the response list to get the UUIDs of each device.
        if 'items' not in response:
            return
        uuids = []
        for item in response['items']:
            if not item['canBeDeployed']:
                pass
            else:
                uuids.append(item)
        return uuids

    def get_deployable_devices(self):
        """Dispose of this method after 20210101."""
        warnings.warn("Deprecated: get_deployable_devices() should be called via deployabledevices().")
        self.deployabledevices()

    def deploymentrequests(self):
        """
        Iterate through the list of devices needing deployed and submit a request to the FMC to deploy changes to them.
        :return:
        """
        logging.debug("In the deploymentrequests() class method.")

        url_suffix = "/deployment/deploymentrequests"
        url = f'{self.configuration_url}{url_suffix}'
        devices = self.deployabledevices()
        if not devices:
            logging.info("No devices need deployed.\n\n")
            return
        json_data = {
            'type': 'DeploymentRequest',
            'forceDeploy': True,
            'ignoreWarning': True,
            'version': str(int(1000000 * datetime.datetime.utcnow().timestamp())),
            'deviceList': []
        }
        for device in devices:
            logging.info(f"Adding device {device} to deployment queue.")
            json_data['deviceList'].append(device['device']['id'])
            # From the list of deployable devices get the version value that is smallest.
            if int(json_data['version']) > int(device['version']):
                logging.info(f"Updating version to {device['version']}")
                json_data['version'] = device['version']

        logging.info("Deploying changes to devices.")
        response = self.send_to_api(method='post', url=url, json_data=json_data)
        return response['deviceList']

    def deploy_changes(self):
        """Dispose of this method after 20210101."""
        warnings.warn("Deprecated: deploy_changes() should be called via deploymentrequests().")
        self.deploymentrequests()


class Token(object):
    """
    The token is the validation object used with the FMC.

    """
    logging.debug("In the Token class.")

    MAX_REFRESHES = 3
    TOKEN_LIFETIME = 60 * 30
    TOKEN_REFRESH_TIME = int(TOKEN_LIFETIME * .95)  # Refresh token at 95% refresh time.
    API_PLATFORM_VERSION = 'api/fmc_platform/v1'

    def __init__(self, host='192.168.45.45', username='admin', password='Admin123', domain=None, verify_cert=False):
        """
        Initialize variables used in the Token class.
        :param host:
        :param username:
        :param password:
        :param verify_cert:
        """
        logging.debug("In the Token __init__() class method.")

        self.__host = host
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.uuid = None
        self.verify_cert = verify_cert
        self.token_refreshes = 0
        self.access_token = None
        self.refresh_token = None
        self.token_creation_time = None
        self.generate_tokens()

    def generate_tokens(self):
        """
        Create new and refresh expired tokens.
        :return:
        """
        logging.debug("In the Token generate_tokens() class method.")

        if self.token_refreshes <= self.MAX_REFRESHES and self.access_token is not None:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.access_token,
                       'X-auth-refresh-token': self.refresh_token}
            url = f'https://{self.__host}/{self.API_PLATFORM_VERSION}/auth/refreshtoken'
            logging.info(f"Refreshing tokens, {self.token_refreshes} out of {self.MAX_REFRESHES} refreshes, "
                         f"from {url}.")
            response = requests.post(url, headers=headers, verify=self.verify_cert)
            logging.debug('Response from refreshtoken post:\n'
                          f'\turl: {url}\n'
                          f'\theaders: {headers}\n'
                          f'\tresponse: {response}')
            self.token_refreshes += 1
        else:
            self.token_refreshes = 0
            self.token_creation_time = datetime.datetime.now()  # Can't trust that your clock is in sync with FMC's.
            headers = {'Content-Type': 'application/json'}
            url = f'https://{self.__host}/{self.API_PLATFORM_VERSION}/auth/generatetoken'
            logging.info(f"Requesting new tokens from {url}.")
            response = requests.post(url, headers=headers,
                                     auth=requests.auth.HTTPBasicAuth(self.__username, self.__password),
                                     verify=self.verify_cert)
            logging.debug('Response from generatetoken post:\n'
                          f'\turl: {url}\n'
                          f'\theaders: {headers}\n'
                          f'\tresponse: {response}')
        self.access_token = response.headers.get('X-auth-access-token')
        self.refresh_token = response.headers.get('X-auth-refresh-token')
        self.uuid = response.headers.get('DOMAIN_UUID')
        all_domain = json.loads(response.headers.get('DOMAINS'))
        if self.__domain is not None:
            for domain in all_domain:
                if 'global/' + self.__domain.lower() == domain['name'].lower():
                    logging.info(f"Domain set to {domain['name']}")
                    self.uuid = domain['uuid']
                else:
                    logging.info("Domain name entered not found in FMC, falling back to Global")

    def get_token(self):
        """
        Check validity of current token.  If needed make a new or refresh.  Then return access_token.
        :return self.access_token
        """
        logging.debug("In the Token get_token() class method.")
        if datetime.datetime.now() > (self.token_creation_time + datetime.timedelta(seconds=self.TOKEN_REFRESH_TIME)):
            logging.info("Token expired.  Generating a new token.")
            self.token_refreshes = 0
            self.access_token = None
            self.refresh_token = None
            self.generate_tokens()

        return self.access_token
