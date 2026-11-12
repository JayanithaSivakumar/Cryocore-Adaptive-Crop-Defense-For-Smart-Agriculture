from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Node:
    node_id: str
    display_name: str
    zone: str
    crop: str
    crop_icon: str
    season: str
    soil_type: str
    irrigation_type: str
    area_acres: float
    latitude: float
    longitude: float
    installed_date: str
    firmware: str
    battery_pct: int
    solar_charging: bool
    lora_rssi: int
    last_seen: str
    status: str
    devices_attached: tuple[str, ...]
    temp_offset: float
    humidity_offset: float
    moisture_offset: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self) | {"devices_attached": list(self.devices_attached)}


_NOW = datetime.now(timezone.utc).isoformat()
_CROPS = {
    "rice": "🌾", "maize": "🌽", "wheat": "🌾", "cotton": "🌿",
    "groundnut": "🥜", "sugarcane": "🎋", "sunflower": "🌻",
}


def demo_nodes() -> list[Node]:
    rows = [
        ("CB-01", "Zone 1", "rice", "Clay", "Flood", 2.0, 0.0, 0.0),
        ("CB-02", "Zone 1", "rice", "Clay", "Flood", 2.0, 0.0, 0.0),
        ("CB-03", "Zone 2", "maize", "Loamy", "Sprinkler", 1.5, -2.0, -4.0),
        ("CB-04", "Zone 2", "maize", "Loamy", "Sprinkler", 1.5, -2.0, -4.0),
        ("CB-05", "Zone 3", "wheat", "Silty", "Drip", 1.0, 1.0, -6.0),
        ("CB-06", "Zone 3", "wheat", "Silty", "Drip", 1.0, 1.0, -6.0),
        ("CB-07", "Zone 4", "cotton", "Sandy", "Drip", 3.0, -8.0, -25.0),
        ("CB-08", "Zone 4", "cotton", "Sandy", "Drip", 3.0, -8.0, -25.0),
        ("CB-09", "Zone 5", "groundnut", "Sandy", "Sprinkler", 0.5, -5.0, -15.0),
        ("CB-10", "Zone 5", "sugarcane", "Loamy", "Flood", 0.5, -1.0, -3.0),
        ("CB-11", "Zone 5", "rice", "Loamy", "Sprinkler", 0.5, -3.0, -8.0),
        ("CB-12", "Zone 5", "rice", "Clay", "Flood", 0.5, 0.0, -2.0),
    ]
    nodes: list[Node] = []
    for index, (node_id, zone, crop, soil, irrigation, temp, humidity, moisture) in enumerate(rows):
        nodes.append(Node(
            node_id=node_id, display_name=f"Sensor {node_id[3:]}", zone=zone,
            crop=crop, crop_icon=_CROPS[crop], season="Kharif", soil_type=soil,
            irrigation_type=irrigation, area_acres=round(1.5 + index * 0.25, 2),
            latitude=11.0168 + index * 0.0012, longitude=76.9558 + index * 0.0011,
            installed_date="2026-06-15", firmware="1.4.2", battery_pct=91 - index * 4,
            solar_charging=index % 3 != 0, lora_rssi=-58 - index * 2,
            last_seen=_NOW, status="low-battery" if index == 10 else "online",
            devices_attached=("heater", "mist", "pump") if crop != "cotton" else ("mist", "pump", "fan"),
            temp_offset=temp, humidity_offset=humidity, moisture_offset=moisture,
        ))
    return nodes


def update_crop(nodes: list[Node], node_id: str, crop: str) -> Node:
    normalized = crop.strip().lower()
    if normalized not in _CROPS:
        raise ValueError(f"Unsupported crop: {crop}")
    for index, node in enumerate(nodes):
        if node.node_id == node_id:
            updated = replace(node, crop=normalized, crop_icon=_CROPS[normalized])
            nodes[index] = updated
            return updated
    raise KeyError(node_id)
