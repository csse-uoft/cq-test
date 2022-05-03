import math
import requests
import time
from datetime import datetime
from .sparql_client import SparqlClient
from .config import GraphDB_BASE_API, REPOSITORY, PASSWORD, USERNAME, SPARQL_ENDPOINT

client = SparqlClient(SPARQL_ENDPOINT, username=USERNAME, password=PASSWORD)


def get_gdb_token(username, password):
    """
    Return a GDB token.
    Used in headers: `Authorization: gdb_token`
    """
    result = requests.post(f'{GraphDB_BASE_API}/rest/login/{username}',
                           headers={'X-GraphDB-Password': password})

    if result.status_code != 200:
        raise ValueError('Wrong username/password')

    return result.headers['Authorization']


def import_ttl(ttl_filename, gdb_token=None):
    with open(ttl_filename, "r") as f:
        data = f.read()

    import_name = f"test data {str(datetime.now())}"

    import_body = {
        "baseURI": None,
        "context": "http://helpseeker.co/test",
        "data": data,
        "forceSerial": False,
        "format": "text/turtle",
        "message": "",
        "name": import_name,
        "parserSettings": {
            "failOnUnknownDataTypes": False,
            "failOnUnknownLanguageTags": False,
            "normalizeDataTypeValues": False,
            "normalizeLanguageTags": False,
            "preserveBNodeIds": False,
            "stopOnError": True,
            "verifyDataTypeValues": False,
            "verifyLanguageTags": True
        },
        "replaceGraphs": [
            "http://helpseeker.co/test"
        ],
        "requestIdHeadersToForward": None,
        "status": "NONE",
        "timestamp": math.trunc(time.time() * 1000),
        "type": "text"
    }
    headers = {'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json'}
    if gdb_token:
        headers['Authorization'] = gdb_token

    result = requests.post(f'{GraphDB_BASE_API}/rest/data/import/upload/{REPOSITORY}/text', json=import_body,
                           headers=headers)
    # print(result.text)

    if result.status_code != 200 and result.status_code != 202:
        raise ValueError("Failed to import file: " + ttl_filename + result.text)

    return import_name


def check_status(name, gdb_token=None):
    """
    Check import status, return True if import is done, False if in progress.
    Raise an error if import is failed or the import does not exist.
    :param gdb_token:
    :param name: import name
    :return: 'DONE' if import is done
    """
    headers = {'Accept': 'application/json, text/plain, */*', 'X-GraphDB-Repository': REPOSITORY}
    if gdb_token:
        headers['Authorization'] = gdb_token
    result = requests.get(GraphDB_BASE_API + '/rest/data/import/upload/' + REPOSITORY, headers=headers)
    result = result.json()
    for imported_item in result:
        if imported_item['name'] == name:
            if imported_item['status'] == 'DONE':
                return True
            elif imported_item['status'] == 'ERROR':
                raise ValueError('Import failed: ' + imported_item['message'])
            else:
                return False
    raise ValueError('Cannot find the import: ' + name)


def delete_import(name, gdb_token=None):
    headers = {'Accept': 'application/json, text/plain, */*', 'X-GraphDB-Repository': REPOSITORY}
    if gdb_token:
        headers['Authorization'] = gdb_token

    body = [name]
    result = requests.delete(GraphDB_BASE_API + f'/rest/data/import/upload/{REPOSITORY}/status?remove=true',
                             headers=headers, json=body)

    if result.status_code != 200:
        raise ValueError("Failed to remove import history: " + name)


def import_ttl_and_wait(filename, username=None, password=None):
    if username and password:
        gdb_token = get_gdb_token(username, password)
    else:
        gdb_token = None
    import_name = import_ttl(filename, gdb_token)

    time.sleep(0.1)
    while not check_status(import_name, gdb_token):
        time.sleep(1)

    delete_import(import_name, gdb_token)
    # print('done')
    return True
