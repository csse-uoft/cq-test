import pytest

from utils.grapgdb import import_ttl_and_wait, client
from utils.config import SPARQL_ENDPOINT, USERNAME, PASSWORD


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

    compass_onto = default_world.get_ontology(
        "https://github.com/csse-uoft/compass-ontology/releases/download/latest/compass.owl"
    ).load(load_all_properties=False, reload=True)


@pytest.mark.order(1)
def test_setup():
    drop_data()
    load_base_ontologies()
    assert import_ttl_and_wait('./data/unit_test.ttl', username=USERNAME, password=PASSWORD)
