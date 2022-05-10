from utils.grapgdb import client
from utils import simplify_uri, assert_list_ignore_order
import pytest


def test_cq1():
    query = """
        # What cp:Organization (s) by cp:Service type exist in my cp:Community
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX cids: <http://ontology.eil.utoronto.ca/cids/cids#>
        PREFIX cp: <http://helpseeker.co/compass#>
        PREFIX i72: <http://ontology.eil.utoronto.ca/ISO21972/iso21972#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX landuse_50872: <http://ontology.eil.utoronto.ca/5087/2/LandUse/>
        PREFIX oep: <http://www.w3.org/2001/sw/BestPractices/OEP/SimplePartWhole/part.owl#>
        
        
        select distinct ?forStakeholder ?forOrg ?forProgram ?forService ?forCode ?location from <http://helpseeker.co/test> where {#} ?forCode ?community ?reqCode where {
            
        # bind(cp:sh_Homeless_Female_Youth_Area1 as ?forStakeholder).
        
            ?forOrg a cp:Organization.
            
            ?forModel cids:hasProgram ?forProgram;
                      cids:forOrganization ?forOrg.
            ?forProgram cids:hasService ?forService.
            ?forService cids:hasCode ?forCode.
            ?forService a cp:Service.
            ?forService cp:hasRequirement ?req.
            {
                ?req cids:hasCode ?reqCode.
            } UNION {
                ?req a cids:CompositeCharacteristic.
                ?req oep:hasPart ?part.
                ?part cids:hasCode ?reqCode.       
            }
            
            ?forProgram cids:hasBeneficialStakeholder ?forStakeholder.
            ?forStakeholder a cids:Stakeholder.
            ?forStakeholder i72:located_in ?location.
            ?forStakeholder cids:hasCharacteristic ?shChar.
            ?shChar cids:hasCode ?shCode.
            
            {
                select ?forService (COUNT(?reqCode) as ?numReqCodes) where {
                { 
                    select distinct ?forService ?reqCode where {
                        ?forService a cp:Service.
                        ?forService cp:hasRequirement ?req.
                        {
                            ?req cids:hasCode ?reqCode.
                        } UNION {
                            ?req a cids:CompositeCharacteristic.
                            ?req oep:hasPart ?part.
                            ?part cids:hasCode ?reqCode.   
                        }
                    }
                }} group by ?forService
            }
            
            FILTER (?shCode = ?reqCode)
            # remove any service that does not require all characteristics of the client
        
        } 
        group by ?forStakeholder ?forOrg ?forProgram ?forService ?forCode ?location ?numReqCodes ?part
        having (count(?shCode) = ?numReqCodes)
        
        order by ?forStakeholder ?forOrg desc(?fundersOrg)  ?forProgram ?forCode ?community ?shCode 
        """

    result = client.execute_sparql(query, infer=True)
    prefix_cp = 'http://helpseeker.co/compass#'

    # stakeholder URI -> list of services
    stakeholder2services = {}

    for data in result['results']['bindings']:
        for_stakeholder = simplify_uri(data['forStakeholder']['value'])
        if not stakeholder2services.get(for_stakeholder):
            stakeholder2services[for_stakeholder] = []
        stakeholder2services[for_stakeholder].append(simplify_uri(data['forService']['value']))

    assert_list_ignore_order(stakeholder2services['cp:sh_Adult_Female_Homeless_Area0'], ['cp:S10-3-Food'])
    assert_list_ignore_order(stakeholder2services['cp:sh_Adult_Female_Homeless_Area1'], ['cp:S12-2-Education'])
    assert_list_ignore_order(stakeholder2services['cp:sh_Adult_Male_Homeless_Area0'], ['cp:S10-3-Food'])
    assert_list_ignore_order(stakeholder2services['cp:sh_Homeless_Female_Youth_Area0'], [
        'cp:S10-1-Shelter', 'cp:S10-2-Shelter', 'cp:S11-1-Food', 'cp:S11-2-Food', 'cp:S11-3-Food'
    ])
    assert_list_ignore_order(stakeholder2services['cp:sh_Homeless_Female_Youth_Area1'], ['cp:S12-1-Education'])
