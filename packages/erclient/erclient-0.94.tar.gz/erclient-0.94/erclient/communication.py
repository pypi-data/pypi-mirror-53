from .base import ErConnector


class Communication(object):

    def __init__(self, communication_id, data=None):
        self.communication_id = communication_id
        if not data:
            # Fetch from remote
            self.refresh()
        else:
            # Allows it to be populated by list_communication_methods without an additional fetch
            self.data = data
            self.refresh(fetch=False)

    def save(self, payload):
        data = self.data
        for item in payload.keys():
            data[item] = payload[item]
        connector = ErConnector()
        url = 'Communication/{communication_id}/'.format(communication_id=self.communication_id)
        response = connector.send_request(
            path=url,
            verb='PUT',
            payload=data
        )
        try:
            self.data = response
            self.refresh(fetch=False) # Don't double-fetch since it returms the object already
            return [True, 'The Communication Method was updated. Item(s) provided were: {items}'.format(
                items=str(payload)
            )]
        except Exception as e:
            return [False, 'An error occured updating the Communication Method. The error was: '.format(e=e)]

    def delete(self):
        return delete_communication_method(self.communication_id)

    def refresh(self, fetch=True):
        if fetch:
            self.data = get_remote_communication(self.communication_id)
        self.type_id = self.data['TypeID']
        self.category_id = self.data['CategoryID']
        self.value = self.data['Value']
        self.is_primary = self.data['IsPrimary']

    def set_value(self, value):
        self.save({'Value':value})
        return [True, 'The Value was updated to {value}'.format(value=self.get_value())]

    def get_value(self):
        return self.data['Value']

    def set_is_primary(self, Value):
        #set a communication method to Primary.
        result = self.save({'IsPrimary':Value})
        self.refresh()
        return result

    def make_primary(self):
        response = self.set_is_primary(True)
        if response[0]:
            return  [True, 'The Communication Method was made primary']
        else:
            return response

class CommunicationCategory(object):

    def __init__(self, data):
        self.data = data
        self.id = self.data['ID']
        self.category_id = self.id
        self.name = self.data['Name']

    def __str__(self):
        return self.name


def get_remote_communication(communication_id):
    # Get a communication with the provided Id
    connector = ErConnector()
    url = 'Communication/{communication_id}/'.format(communication_id=communication_id)
    response = connector.send_request(
        path=url
    )
    return response


def list_communication_methods(type, id, about_id=None, is_primary=False):
    # Retrieves a list of Valid Communication Types. This list will include both built-in Communication Types and Custom.
    connector = ErConnector()  # 2.0 API
    url = 'Communication/ByAboutId/{type}/{id}'.format(
        type=type,
        id=id
    )
    response = connector.send_request(
        path=url,
        verb='GET'
    )
    methods = [Communication(communication_id=method['ID'], data=method) for method in response]

    if about_id:
        methods = [method for method in methods if method.type_id == about_id]

    if is_primary:
        methods = [method for method in methods if method.is_primary is True]

    return methods

def list_communication_categories(name=None):
    connector = ErConnector()  # 2.0 API
    url = 'Communication/Category'

    response = connector.send_request(
        path=url,
        verb='GET'
    )

    categories = [CommunicationCategory(category) for category in response]
    if name:
        categories = [category for category in categories if category.name == name]
        return categories[0]
    else:
        return categories

def delete_communication_method(communication_id):
    connector = ErConnector()
    url = 'Communication/{communication_id}/'.format(communication_id=communication_id)
    response = connector.send_request(
        path=url,
        verb='DELETE',
        rawresponse=True
    )
    if response.status_code == 204:

        return (True, "The Communication Method was deleted successfully")
    else:
        return (False, response.json()['Message'])

def add_communication_method(abouttype_id, type_id, obj_id, value, is_primary=False):
    connector = ErConnector()
    url = 'Communication/{abouttype_id}/{obj_id}/'.format(
        abouttype_id=abouttype_id,
    obj_id=obj_id)
    data = {}
    data['AboutType'] = abouttype_id
    data['Id'] = obj_id
    data['TypeID'] = type_id
    data['Value'] = value
    data['IsPrimary'] = is_primary
    response = connector.send_request(
        path=url,
        verb='POST',
        payload=data
    )

    return response
