from functools import lru_cache

from .base import ErConnector

class SubCategory(object):

    def __init__(self, subcategory_id, data=None):
        self.subcategory_id = subcategory_id
        if not data:
            # Fetch from remote
            self.refresh()
        else:
            # Allows it to be populated by list methods without an additional fetch
            self.data = data
        self.populate_from_data()

    def refresh(self):
        self.data = get_subcategory_by_id(self.subcategory_id).data
        self.populate_from_data()

    def populate_from_data(self):
        self.name = self.data.get('Name', None)

def get_subcategory_by_id(subcategory_id):
    connector = ErConnector()  # 2.0 API
    url = 'FolderGroup/SubCategory/{id}'.format(
        id=subcategory_id,
    )
    response = connector.send_request(
        path=url,
        verb='GET',
    )

    return SubCategory(response['ID'], data=response)


def list_subcategories():
    connector = ErConnector()
    url = 'FolderGroup/SubCategory/'
    response = connector.send_request(
        path=url,
        verb='GET',
    )
    return [SubCategory(subcategory_id=data['ID'], data=data) for data in response]
