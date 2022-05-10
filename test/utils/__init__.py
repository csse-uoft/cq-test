prefixes = {
    'cp:': 'http://helpseeker.co/compass#',
    'cids:': 'http://ontology.eil.utoronto.ca/cids/cids',
    'i72:': 'http://ontology.eil.utoronto.ca/ISO21972/iso21972#',
}


def simplify_uri(uri: str):
    for prefix, namespace in prefixes.items():
        if uri.startswith(namespace):
            return prefix + uri[len(namespace):]


def assert_list_ignore_order(l1, l2):
    assert sorted(l1) == sorted(l2)
