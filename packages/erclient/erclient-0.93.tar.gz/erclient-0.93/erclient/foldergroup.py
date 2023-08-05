from functools import lru_cache

from .base import ErConnector

from .category import Category
from .subcategory import SubCategory

class FolderGroup(object):

    def __init__(self, foldergroup_id, data=None):
        self.foldergroup_id = foldergroup_id
        if not data:
            # Fetch from remote
            self.refresh()
        else:
            # Allows it to be populated by list methods without an additional fetch
            self.data = data
        self.populate_from_data()

    def refresh(self):
        self.data = get_foldergroup_by_id(self.foldergroup_id).data
        self.populate_from_data()

    def populate_from_data(self):
        self.name = self.data.get('Name', None)
        self.category_id = self.data.get('CategoryID', None)
        self.subcategory_id = self.data.get('SubCategoryID', None)

    def category(self):
        return Category(category_id=self.category_id)
    def subcategory(self):
        return SubCategory(subcategory_id=self.subcategory_id)

def get_foldergroup_by_id(foldergroup_id):
    connector = ErConnector()  # 2.0 API
    url = 'FolderGroup/{id}'.format(
        id=foldergroup_id,
    )
    response = connector.send_request(
        path=url,
        verb='GET',
    )

    return FolderGroup(response['ID'])


def list_foldergroups(category_id=None, subcategory_id=None):
    connector = ErConnector()
    url = 'FolderGroup/?CategoryId=29'
    response = connector.send_request(
        path=url,
        verb='GET',
    )
    return [FolderGroup(foldergroup_id=data['ID'], data=data) for data in response]
