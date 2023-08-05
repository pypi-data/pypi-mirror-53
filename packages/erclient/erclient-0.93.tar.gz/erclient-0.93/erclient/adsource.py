from .base import ErConnector

def list_adsources(abouttype_id):
    connector = ErConnector()
    url = 'AdSource/{abouttype_id}/'.format(abouttype_id=abouttype_id)
    response = connector.send_request(
        path=url,
        verb='GET',
    )
    return response

def get_adsource_id_from_name(abouttype_id, name):
    try:
        return [x for x in list_adsources(abouttype_id) if x['Name'] == name][0]['ID']
    except:
        return None