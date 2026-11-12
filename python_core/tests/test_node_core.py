from crop_bodyguard_core.registry import demo_nodes, update_crop
from crop_bodyguard_core.service import overview_for, reading_for, risk_for


def test_registry_has_twelve_nodes_five_zones_and_six_crops():
    nodes = demo_nodes()
    assert len(nodes) == 12
    assert len({node.zone for node in nodes}) == 5
    assert len({node.crop for node in nodes}) == 6


def test_frost_targets_zone_three_nodes_only():
    nodes = demo_nodes()
    frost = [node for node in nodes if overview_for(node, "Frost night")["risk"]["hazard"] == "frost"]
    assert {node.node_id for node in frost} == {"CB-05", "CB-06"}
    assert all(overview_for(node, "Frost night")["reading"]["temperature"] == 2.8 for node in frost)


def test_hot_dry_node_has_drought_and_heat_context():
    node = next(node for node in demo_nodes() if node.node_id == "CB-07")
    overview = overview_for(node, "Heat wave")
    assert overview["reading"]["temperature"] == 42.0
    assert overview["risk"]["status"] == "DANGER"
    assert overview["node"]["crop"] == "cotton"


def test_crop_edit_recomputes_identity_and_ideal_profile():
    nodes = demo_nodes()
    update_crop(nodes, "CB-09", "sunflower")
    overview = overview_for(next(node for node in nodes if node.node_id == "CB-09"))
    assert overview["node"]["crop"] == "sunflower"
    assert overview["risk"]["ideal"]["max_temperature"] == 35.0
