from owlready2 import default_world


default_world.set_backend(backend="sparql-endpoint",
                          endpoint="http://127.0.0.1:7200/repositories/cq-test", debug=False)
                          # endpoint="http://3.97.83.181:7200/repositories/cq-test", debug=False,
                          # username='admin', password='admin')

compass_onto = default_world.get_ontology(
    "https://github.com/csse-uoft/compass-ontology/releases/download/latest/compass.owl"
).load(load_all_properties=False, reload=True)

