from utils.grapgdb import client
from utils import simplify_uri, assert_list_ignore_order
import pytest


def test_cq1():
    query = """
        # what are the funding flows for the organizations broken down by cp:Stakeholder type?
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX cids: <http://ontology.eil.utoronto.ca/cids/cids#>
        PREFIX cp: <http://helpseeker.co/compass#>
        PREFIX i72: <http://ontology.eil.utoronto.ca/ISO21972/iso21972#>
        # ?StakeholderType ?forProgram  ?fundersProgram
        select distinct ?stakeholderType ?forOrg ?fundersOrg ?area where {
        #    bind(cp:CL-Homeless as ?stakeholderType)
            
            ?fundersOrg a cp:Organization.
            ?fundersModel cids:forOrganization ?fundersOrg.
            ?fundersModel cids:hasProgram ?fundersProgram.
            
            ?forOrg a cp:Organization.
            ?forModel cids:forOrganization ?forOrg.
            ?forModel cids:hasProgram ?forProgram.
            
            ?funding a cp:Funding.
            ?funding cp:forProgram ?forProgram.
            ?funding cids:forStakeholder ?forStakeholder.
            ?forStakeholder cids:hasCharacteristic ?characteristic.
            ?characteristic cids:hasCode ?stakeholderType.
            # The program that provides the funding
            ?funding cp:fundersProgram ?fundersProgram.
            ?forStakeholder i72:located_in ?area.
            
        } order by ?stakeholderType
        """

    result = client.execute_sparql(query, infer=True)
    prefix_cp = 'http://helpseeker.co/compass#'

    # stakeholder URI -> (fundersOrg, forOrg)
    stakeholder_type2services = {}

    for data in result['results']['bindings']:
        stakeholder_type = simplify_uri(data['stakeholderType']['value'])
        if not stakeholder_type2services.get(stakeholder_type):
            stakeholder_type2services[stakeholder_type] = []
        stakeholder_type2services[stakeholder_type].append(
            (simplify_uri(data['fundersOrg']['value']), simplify_uri(data['forOrg']['value']))
        )

    assert len(stakeholder_type2services['cp:CL-Adult']) == 5
    assert len(stakeholder_type2services['cp:CL-Female']) == 8
    assert len(stakeholder_type2services['cp:CL-Funder']) == 6
    assert len(stakeholder_type2services['cp:CL-Homeless']) == 8
    assert len(stakeholder_type2services['cp:CL-Male']) == 8

