from functools import lru_cache

from .base import ErConnector

class Category(object):

    def __init__(self, category_id, data=None):
        self.category_id = category_id
        if not data:
            # Fetch from remote
            self.refresh()
        else:
            # Allows it to be populated by list methods without an additional fetch
            self.data = data
        self.populate_from_data()

    def refresh(self):
        self.data = get_category_by_id(self.category_id).data
        self.populate_from_data()

    def populate_from_data(self):
        self.name = self.data.get('Name', None)

def get_category_by_id(category_id):
    connector = ErConnector()  # 2.0 API
    url = 'FolderGroup/Category/{id}'.format(
        id=category_id,
    )
    response = connector.send_request(
        path=url,
        verb='GET',
    )

    return Category(response['ID'], data=response)


def list_categories():
    connector = ErConnector()
    url = 'FolderGroup/Category/'
    response = connector.send_request(
        path=url,
        verb='GET',
    )
    return [Category(category_id=data['ID'], data=data) for data in response]
