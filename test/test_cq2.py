from utils.grapgdb import client
from utils import simplify_uri, assert_list_ignore_order
import pytest


def test_cq2():
    query = """
        # what are the funding flows for the organizations broken down by cp:Stakeholder type?
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX cids: <http://ontology.eil.utoronto.ca/cids/cids#>
        PREFIX cp: <http://helpseeker.co/compass#>
        PREFIX i72: <http://ontology.eil.utoronto.ca/ISO21972/iso21972#>
        PREFIX landuse_50872: <http://ontology.eil.utoronto.ca/5087/2/LandUse/>
        select distinct ?forOrg ?fundersOrg ?area ?forCode where {
            
            ?fundersOrg a cp:Organization.
            ?fundersModel cids:forOrganization ?fundersOrg.
            ?fundersModel cids:hasProgram ?fundersProgram.
            
            ?forOrg a cp:Organization.
            ?forModel cids:forOrganization ?forOrg.
            ?forModel cids:hasProgram ?forProgram.
            
            ?funding a cp:Funding.
            ?funding cp:forProgram ?forProgram.
            ?forProgram cids:hasService ?forService.
            ?forService cids:hasCode ?forCode.
            ?forService cids:hasBeneficialStakeholder ?sh.
            ?sh i72:located_in ?area.
            
            # The program that provides the funding
            ?funding cp:fundersProgram ?fundersProgram.
        }
        """

    result = client.execute_sparql(query, infer=True)
    assert len(result['results']['bindings']) > 0

    # stakeholder URI -> (fundersOrg, forOrg)
    for_code2services = {}

    for data in result['results']['bindings']:
        for_code = f"{simplify_uri(data['forCode']['value'])} @ {simplify_uri(data['area']['value'])}"
        if not for_code2services.get(for_code):
            for_code2services[for_code] = []
        for_code2services[for_code].append(
            (simplify_uri(data['fundersOrg']['value']), simplify_uri(data['forOrg']['value']))
        )
    assert_list_ignore_order(for_code2services['cp:CL-Shelter @ cp:Area0_Location'], [('cp:Org20', 'cp:Org10')])
    assert_list_ignore_order(for_code2services['cp:CL-Health @ cp:Area1_Location'], [('cp:Org50', 'cp:Org13')])
    assert_list_ignore_order(for_code2services['cp:CL-Funding @ cp:Area0_Location'],
                             [('cp:Org100', 'cp:Org20'), ('cp:Org100', 'cp:Org30'), ('cp:Org100', 'cp:Org50')])
    assert_list_ignore_order(for_code2services['cp:CL-Funding @ cp:Area1_Location'],
                             [('cp:Org100', 'cp:Org40'), ('cp:Org100', 'cp:Org50')])
    assert_list_ignore_order(for_code2services['cp:CL-Food @ cp:Area0_Location'],
                             [('cp:Org20', 'cp:Org11'), ('cp:Org20', 'cp:Org10'), ('cp:Org30', 'cp:Org11'),
                              ('cp:Org50', 'cp:Org11')])
    assert_list_ignore_order(for_code2services['cp:CL-Food @ cp:Area1_Location'], [('cp:Org50', 'cp:Org13')])
    assert_list_ignore_order(for_code2services['cp:CL-Education @ cp:Area1_Location'], [('cp:Org40', 'cp:Org12')])
