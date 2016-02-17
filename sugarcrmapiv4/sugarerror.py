#
#   sugarerror.py
#
#   Exceptions to be raised when various problems occur while running sugarcrm software
#

class SugarError(Exception):
    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        self.number = data['number']

    @property
    def is_invalid_session(self):
        return self.number == 11

    @property
    def is_invalid_login(self):
        return self.number == 10

    @property
    def is_missing_module(self):
        return self.number == 20

    @property
    def is_null_response(self):
        return self.number == 0

    @property
    def is_invalid_request(self):
        return self.number == 1001

class SugarUnhandledException(Exception):
    pass


def is_error(data):
    try:
        if data['name'] in ('Module Does Not Exist',):
            return True
        return data["name"] != None and data["description"] != None
    except KeyError:
        return False
