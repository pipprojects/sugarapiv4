#
from six.moves import urllib
import hashlib
import json
from .sugarerror import SugarError, SugarUnhandledException, is_error
#
class SugarAPI:

    def __init__(self, url, username, password, is_ldap_member = False):

        # String which holds the session id of the connection, required at
        # every call after 'login'.
        self._session = ""

        # url which is is called every time a request is made.
        self._url = url

        self._username = username
        self._password = password
        self._isldap = is_ldap_member
#
        self._methods = {
            "get_entry_list":
                ["session", "module_name", "query", "order_by", "offset", "select_fields", "link_name_to_fields_array", "max_results", "deleted", "favorites"],
            "set_entry":
                ["session", "module_name", "name_value_list"],
        }

        # Attempt to login.
        #self._login()
        self.login()

        # Dynamically add the API methods to the object.
        #for method in ['get_user_id', 'get_user_team_id',
        #               'get_available_modules', 'get_module_fields',
        #               'get_entries_count', 'get_entry', 'get_entries',
        #               'get_entry_list', 'set_entry', 'set_entries',
        #               'set_relationship', 'set_relationships',
        #               'get_relationships', 'get_server_info',
        #               'set_note_attachment', 'get_note_attachment',
        #               'set_document_revision', 'get_document_revision',
        #               'search_by_module', 'get_report_entries', 'logout']:


    def call(self, method_name, argsin, Native=False):
#
        if not Native:
            args = self._setArguments(method_name, argsin)
        else:
            args = argsin[:]
#
        #print args
        #print "Args %s" %([self._session] + list(args))
        try:
            result = self._sendRequest(method_name,
                                              [self._session] + list(args))
            print "Info: Sent request"

            #print result
        except SugarError as error:
#
            print "Warning: Could not send request"
#
            if error.is_invalid_session:
                # Try to recover if session ID was lost
                self.login()
                result = self._sendRequest(method_name, [self._session] + list(args))
            elif error.is_missing_module:
                return None
            elif error.is_null_response:
                return None
            elif error.is_invalid_request:
                print method_name, args
            else:
                raise SugarUnhandledException('%d, %s - %s' %
                                                      (error.number,
                                                       error.name,
                                                       error.description))

        return result

    def _sendRequest(self, method, data):

        data = json.dumps(data)
        args = {'method': method, 'input_type': 'json',
                'response_type' : 'json', 'rest_data' : data}
        params = urllib.parse.urlencode(args).encode('utf-8')
        response = urllib.request.urlopen(self._url, params)
        response = response.read().strip()
        if not response:
            raise SugarError({'name': 'Empty Result',
                              'description': 'No data from SugarCRM.',
                              'number': 0})
        result = json.loads(response.decode('utf-8'))
        if is_error(result):
            raise SugarError(result)
        return result

    def login(self):

        args = {'user_auth': {'user_name': self._username,
                              'password': self.password()}}

        x = self._sendRequest('login', args)

        try:
            self._session = x['id']
        except KeyError:
            raise SugarUnhandledException

    def password(self):

        if self._isldap:
            return self._password
        encode = hashlib.md5(self._password.encode('utf-8'))
        result = encode.hexdigest()

        return result
#
# Set up arguments list for each method call
#
    def _setArguments(self, method_name, Args):
        arguments = []
        for entry in self._methods[method_name]:
            if entry != "session":
                if entry in Args:
                    param = Args[entry]
                else:
                    param = ""
                arguments.append(param)
        return arguments
#
# Create
#
    def Create_Record(self, Args={}):
        if "id" in Args["name_value_list"]:
            del Args["name_value_list"]["id"]
        return self.call("set_entry", Args)
#
# Read
#
    def Read_Record(self, Args={}):
        return self.call("get_entry_list", Args)

    def Read_Record_By_ID(self, ID, Args={}, Table=''):
        if not Table:
            Table = Args["module_name"].lower()
        Args["query"] = "%s.id = '%s'" %(Table, ID)
        #print json.dumps(Args, sort_keys=True, indent=4, separators=(',', ': '))
        return self.call("get_entry_list", Args)
#
# Update
#
    def Update_Record_By_ID(self, ID, Args={}):
        Args["name_value_list"]["id"] = ID
        return self.call("set_entry", Args)
#
