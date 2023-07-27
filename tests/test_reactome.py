from src.controllers.biopax_controller import BiopaxController

parser_type = "reactome"


def test_chebi_extraction():
    controller = BiopaxController()
    biopax_path = "resources/test_biopax/reactome/R-HSA-204174_level3.owl"
    parsed_data = controller.process_biopax_file(parser_type, biopax_path)

    found_chebis = []
    for pthwy in parsed_data.pathways:
        for rxn in pthwy.reactions:
            for c in rxn.controllers:
                if c.id.lower().startswith("chebi"):
                    found_chebis.append(c.id)

    # Hint: it's in the xrefs of entity_reference of controller NADH
    assert 'CHEBI:57945' in found_chebis
