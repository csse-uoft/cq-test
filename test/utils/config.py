import os

GraphDB_BASE_API = os.getenv('GDB_BASE_API') or 'http://3.97.83.181:7200'  # 'http://3.97.83.181:7200'
REPOSITORY = os.getenv('GDB_REPO') or 'cq-test'
USERNAME = os.getenv('GDB_USERNAME') or None
PASSWORD = os.getenv('GDB_PASSWORD') or None

SPARQL_ENDPOINT = f'{GraphDB_BASE_API}/repositories/{REPOSITORY}'
BASE_ONTOLOGY_LOCATION = 'https://github.com/csse-uoft/compass-ontology/releases/download/latest/compass.owl'
TEST_DATA_LOCATION = 'https://github.com/csse-uoft/csv2turtle/releases/download/latest/unit_test3.ttl'
