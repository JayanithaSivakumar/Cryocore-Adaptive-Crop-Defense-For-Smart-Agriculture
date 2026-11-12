from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from crop_bodyguard_core.registry import Node, demo_nodes, update_crop
from crop_bodyguard_core.service import overview_for, reading_for

app = FastAPI(title="Crop Bodyguard Python Intelligence Core", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
NODES: list[Node] = demo_nodes()
SCENARIO = "All clear"
ALERTS: list[dict[str, Any]] = []


class ScenarioRequest(BaseModel):
    scenario: str = "All clear"
    node_ids: list[str] = Field(default_factory=list)


class DeviceCommand(BaseModel):
    state: str
    duration_min: int = 30
    mode: str = "manual"


class RegisterNode(BaseModel):
    node_id: str
    display_name: str
    zone: str
    crop: str
    soil_type: str = "Loamy"
    irrigation_type: str = "Drip"


def find_node(node_id: str) -> Node:
    for node in NODES:
        if node.node_id == node_id:
            return node
    raise HTTPException(status_code=404, detail=f"Unknown node: {node_id}")


@app.get("/api/farm/summary")
def farm_summary() -> dict[str, Any]:
    online = sum(node.status == "online" for node in NODES)
    return {"farm_name": "Coimbatore Demo Farm", "district": "coimbatore", "demo": True, "device_count": len(NODES), "zone_count": len({node.zone for node in NODES}), "crop_count": len({node.crop for node in NODES}), "online": online, "offline": len(NODES) - online, "low_battery": sum(node.battery_pct < 30 for node in NODES), "nodes": nodes_list()}


def nodes_list() -> list[dict[str, Any]]:
    return [{"node": node.as_dict(), "reading": overview_for(node, SCENARIO)["reading"], "risk": overview_for(node, SCENARIO)["risk"]} for node in NODES]


@app.get("/api/nodes")
def list_nodes() -> list[dict[str, Any]]:
    return nodes_list()


@app.get("/api/nodes/{node_id}/overview")
def node_overview(node_id: str) -> dict[str, Any]:
    return overview_for(find_node(node_id), SCENARIO)


@app.get("/api/nodes/{node_id}/history")
def node_history(node_id: str, range: str = "24h", agg: str = "1m") -> dict[str, Any]:
    node = find_node(node_id)
    current = reading_for(node, SCENARIO)
    points = 24 if range == "24h" else 7
    return {"node_id": node_id, "range": range, "aggregation": agg, "points": [{"period": index, "temperature": round(current.temperature + (index % 4 - 2) * 0.7, 1), "soil_moisture": round(current.soil_moisture + (index % 3 - 1) * 1.2, 1)} for index in range(points)]}


@app.get("/api/nodes/compare")
def compare_nodes(a: str, b: str) -> dict[str, Any]:
    first, second = find_node(a), find_node(b)
    first_reading, second_reading = reading_for(first, SCENARIO), reading_for(second, SCENARIO)
    return {"a": {"node": first.as_dict(), "reading": first_reading.as_dict()}, "b": {"node": second.as_dict(), "reading": second_reading.as_dict()}, "temperature_difference": round(first_reading.temperature - second_reading.temperature, 1)}


@app.get("/api/nodes/{node_id}")
def node_detail(node_id: str) -> dict[str, Any]:
    return find_node(node_id).as_dict()


@app.get("/api/nodes/{node_id}/alerts")
def node_alerts(node_id: str) -> list[dict[str, Any]]:
    find_node(node_id)
    return [alert for alert in ALERTS if alert["node_id"] == node_id]


@app.post("/api/nodes/{node_id}/devices/{device}")
def node_device(node_id: str, device: str, command: DeviceCommand) -> dict[str, Any]:
    node = find_node(node_id)
    return {"ok": True, "node_id": node.node_id, "device": device, "command": command.model_dump(), "queued": False}


@app.post("/api/nodes/register")
def register_node(payload: RegisterNode) -> dict[str, Any]:
    if any(node.node_id == payload.node_id for node in NODES):
        raise HTTPException(status_code=409, detail="Node already registered")
    node = Node(node_id=payload.node_id, display_name=payload.display_name, zone=payload.zone, crop=payload.crop.lower(), crop_icon="🌿", season="Kharif", soil_type=payload.soil_type, irrigation_type=payload.irrigation_type, area_acres=1.0, latitude=11.0168, longitude=76.9558, installed_date=datetime.now(timezone.utc).date().isoformat(), firmware="1.0.0", battery_pct=100, solar_charging=True, lora_rssi=-55, last_seen=datetime.now(timezone.utc).isoformat(), status="online", devices_attached=("heater", "pump"), temp_offset=0, humidity_offset=0, moisture_offset=0)
    NODES.append(node)
    return node.as_dict()


@app.patch("/api/nodes/{node_id}")
def patch_node(node_id: str, crop: str | None = None) -> dict[str, Any]:
    find_node(node_id)
    if crop:
        return update_crop(NODES, node_id, crop).as_dict()
    return find_node(node_id).as_dict()


@app.post("/api/simulate")
def simulate(payload: ScenarioRequest) -> dict[str, Any]:
    global SCENARIO
    SCENARIO = payload.scenario
    targets = set(payload.node_ids)
    affected = [node for node in NODES if not targets or node.node_id in targets]
    for node in affected:
        overview = overview_for(node, SCENARIO)
        if overview["risk"]["status"] == "DANGER":
            ALERTS.insert(0, {"id": f"{node.node_id}-{len(ALERTS)}", "node_id": node.node_id, "zone": node.zone, "crop": node.crop, "hazard": overview["risk"]["hazard"], "severity": "DANGER", "message": f"Node {node.node_id}. {node.crop}. {overview['risk']['hazard']} danger.", "acknowledged": False, "time": datetime.now(timezone.utc).isoformat()})
    return {"scenario": SCENARIO, "affected_nodes": [node.node_id for node in affected]}


@app.post("/api/alerts/{alert_id}/ack")
def acknowledge(alert_id: str) -> dict[str, Any]:
    for alert in ALERTS:
        if alert["id"] == alert_id:
            alert["acknowledged"] = True
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Unknown alert")


@app.post("/api/ingest")
def ingest(packet: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "accepted": True, "node_id": packet.get("Node ID") or packet.get("node_id"), "message": "Packet accepted at the Python gateway boundary."}


@app.websocket("/live")
async def live(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        await websocket.send_json({"timestamp": datetime.now(timezone.utc).isoformat(), "nodes": nodes_list()})
        await asyncio.sleep(5)
