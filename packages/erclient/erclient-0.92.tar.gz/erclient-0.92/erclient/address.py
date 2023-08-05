from .base import ErConnector

class Address(object):

    def __init__(self, address_id, data=None):
        self.address_id = address_id
        self.data = None
        if not data:
            # Fetch from remote
            self.refresh()
        else:
            # Allows it to be populated by list_communication_methods without an additional fetch
            self.data = data
            self.populate_from_data()

    def refresh(self):
        self.data = get_address_by_id(self.address_id).data
        self.populate_from_data()

    def populate_from_data(self):
        self.address_line_1 = self.data.get('AddressLine1', None)
        self.address_line_2 = self.data.get('AddressLine2', None)
        self.city = self.data.get('City', None)

    def delete(self):
        return delete_address(self.address_id)

def list_addresses(type, id):
    connector = ErConnector()  # 2.0 API
    url = 'Address/{AboutType}/{id}'.format(
        AboutType=type,
        id=id
    )
    response = connector.send_request(
        path=url,
    )

    return [Address(address_id=address['AddressID'], data=address) for address in response]


def add_address(
        abouttype_id,
        type_id,
        obj_id,
        address_line_1,
        city,
        state_id,
        region_id,
        postal_code,
        address_line_2=None,
        country_id=220
):
    connector = ErConnector()  # 2.0 API
    url = 'Address/{AboutType}/{Id}'.format(
        AboutType=abouttype_id,
        Id=obj_id,

    )

    data = {
            'AddressLine1': address_line_1,
            'AddressLine2': address_line_2,
            'City': city,
            'PostalCode': postal_code,
            'StateID': state_id,
            'CountryID': country_id,
            'RegionID': region_id,
            'TypeID': type_id}

    response = connector.send_request(
        path=url,
        verb='POST',
        payload=data
    )

    return response


def get_address_by_id(id, pathonly=False):
    connector = ErConnector()  # 2.0 API
    url = 'Address/{Id}/'.format(
        Id=id
    )
    response = connector.send_request(
        path=url,
    )

    return Address(response['AddressID'], data=response)


def delete_address(id):
    connector = ErConnector()  # 2.0 API
    url = 'Address/{id}/'.format(
        id=id
    )
    response = connector.send_request(
        path=url,
        verb='DELETE',
        rawresponse=True
    )

    if response.status_code == 204:

        return (True, "The Address was deleted successfully")
    else:
        return response

def list_address_regions():
    connector = ErConnector()  # 2.0 API
    url = 'Address/Region/'
    response = connector.send_request(
        path=url,
    )

    return response

def get_address_region_id_by_name(name):
    try:
        return [x for x in list_address_regions() if x['Name'] == name][0]['ID']
    except:
        return None

def list_address_states():
    connector = ErConnector()  # 2.0 API
    url = 'Address/State/'
    response = connector.send_request(
        path=url,
    )

    return response

def get_address_state_id_by_name(name):
    try:
        return [x for x in list_address_states() if x['Name'] == name][0]['ID']
    except:
        return None

def list_address_countries():
    connector = ErConnector()  # 2.0 API
    url = 'Address/Country/'
    response = connector.send_request(
        path=url,
    )

    return response

def get_address_country_id_by_name(name):
    try:
        return [x for x in list_address_countries() if x['Name'] == name][0]['ID']
    except:
        return None

def list_address_types():
    connector = ErConnector()  # 2.0 API
    url = 'Address/Type/'
    response = connector.send_request(
        path=url,
    )

    return response

def get_address_type_id_by_name(name):
    try:
        return [x for x in list_address_types() if x['Name'] == name][0]['ID']
    except:
        return None