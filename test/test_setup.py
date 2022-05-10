import pytest
import urllib.request
import os

from utils.grapgdb import import_ttl_and_wait, client
from utils.config import SPARQL_ENDPOINT, USERNAME, PASSWORD, TEST_DATA_LOCATION, BASE_ONTOLOGY_LOCATION

dir_path = os.path.dirname(os.path.realpath(__file__))
turtle_file_path = f"{dir_path}/../unit_test.ttl"


def download_test_data():
    urllib.request.urlretrieve(TEST_DATA_LOCATION, turtle_file_path)


def drop_data():
    client.execute_sparql("CLEAR ALL")
    result = client.execute_sparql("""
    select * where { 
	    ?s ?p ?o .
    } limit 1""", infer=False)
    assert len(result["results"]["bindings"]) == 0


def load_base_ontologies():
    from owlready2 import default_world

    default_world.set_backend(backend="sparql-endpoint",
                              endpoint=SPARQL_ENDPOINT, debug=False,
                              # endpoint="http://3.97.83.181:7200/repositories/cq-test", debug=False,
                              username=USERNAME, password=PASSWORD)

    compass_onto = default_world.get_ontology(BASE_ONTOLOGY_LOCATION).load(load_all_properties=False, reload=True)


@pytest.mark.order(1)
def test_setup():
    drop_data()
    load_base_ontologies()
    download_test_data()
    assert import_ttl_and_wait(turtle_file_path, username=USERNAME, password=PASSWORD)
