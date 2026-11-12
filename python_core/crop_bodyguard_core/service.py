from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .registry import Node


@dataclass(frozen=True)
class Reading:
    temperature: float
    humidity: float
    soil_moisture: float
    soil_temperature: float
    wind: float
    rain: float
    solar: float

    def as_dict(self) -> dict[str, float]:
        return {
            "temperature": round(self.temperature, 1), "humidity": round(self.humidity, 1),
            "soil_moisture": round(self.soil_moisture, 1), "soil_temperature": round(self.soil_temperature, 1),
            "wind": round(self.wind, 1), "rain": round(self.rain, 1), "solar": round(self.solar, 1),
        }


IDEALS: dict[str, tuple[float, float, float]] = {
    "rice": (20.0, 35.0, 70.0), "maize": (18.0, 32.0, 65.0), "wheat": (12.0, 27.0, 60.0),
    "cotton": (21.0, 38.0, 55.0), "groundnut": (20.0, 32.0, 60.0), "sugarcane": (20.0, 36.0, 70.0),
    "sunflower": (18.0, 35.0, 55.0),
}


def reading_for(node: Node, scenario: str = "All clear") -> Reading:
    base = Reading(temperature=27.0, humidity=63.0, soil_moisture=51.0, soil_temperature=25.0, wind=2.8, rain=0.0, solar=58.0)
    reading = Reading(base.temperature + node.temp_offset, base.humidity + node.humidity_offset, base.soil_moisture + node.moisture_offset, base.soil_temperature + node.temp_offset / 2, base.wind, base.rain, base.solar)
    if scenario == "Frost night" and node.zone == "Zone 3":
        return Reading(2.8, 94.0, reading.soil_moisture, 7.0, 1.1, 0.0, 4.0)
    if scenario == "Heat wave" and node.zone == "Zone 4":
        return Reading(42.0, 25.0, reading.soil_moisture, 34.0, 4.8, 0.0, 94.0)
    if scenario == "Drought" and node.node_id == "CB-07":
        return Reading(35.0, 31.0, 10.0, 30.0, 3.2, 0.0, 82.0)
    if scenario == "Heavy rain" and node.zone == "Zone 5":
        return Reading(25.0, 93.0, reading.soil_moisture, 24.0, 2.0, 48.0, 8.0)
    return reading


def risk_for(node: Node, reading: Reading) -> dict[str, Any]:
    t_min, t_max, humidity_ideal = IDEALS[node.crop]
    frost = max(0.0, min(100.0, (t_min - reading.temperature) * 12 + (reading.humidity - 80) * 0.7))
    heat = max(0.0, min(100.0, (reading.temperature - t_max) * 15 + (reading.solar - 70) * 0.5))
    drought_threshold = 25.0 if node.soil_type == "Sandy" else 20.0
    drought = max(0.0, min(100.0, (drought_threshold - reading.soil_moisture) * 4))
    rain = max(0.0, min(100.0, (reading.rain - 25) * 3.2))
    risks = {"frost": round(frost), "heat": round(heat), "drought": round(drought), "heavy_rain": round(rain)}
    hazard, score = max(risks.items(), key=lambda item: item[1])
    status = "DANGER" if score >= 70 else "WATCH" if score >= 25 else "SAFE"
    return {"status": status, "hazard": hazard if score else "all_clear", "overall_pct": score, "risks": risks, "trend": "rising" if score >= 50 else "steady", "ideal": {"min_temperature": t_min, "max_temperature": t_max, "humidity": humidity_ideal}}


def overview_for(node: Node, scenario: str = "All clear") -> dict[str, Any]:
    reading = reading_for(node, scenario)
    risk = risk_for(node, reading)
    feels_like = reading.temperature + (reading.humidity - 50) * 0.04
    description = "Very cold, frost likely" if risk["hazard"] == "frost" else "Hot and dry, strong sun" if risk["hazard"] == "heat" else "Very dry soil, irrigation needed" if risk["hazard"] == "drought" else "Rainfall-prone, irrigation paused" if risk["hazard"] == "heavy_rain" else "Comfortable growing conditions"
    advice = {"frost": "Switch the heater on and delay irrigation.", "heat": "Use mist only if humidity is low; keep the crop shaded.", "drought": "Start targeted irrigation for this node.", "heavy_rain": "Keep mist and irrigation locked while rain continues.", "all_clear": "Keep Guardian Mode on and continue monitoring."}[risk["hazard"]]
    return {"node": node.as_dict(), "reading": reading.as_dict(), "weather": {"description": description, "feels_like": round(feels_like, 1), "dew_point_estimate": round(reading.temperature - (100 - reading.humidity) / 5, 1), "estimated_rain_wind": True}, "risk": risk, "recommendation": advice, "devices": {device: {"state": "off", "mode": "auto", "locked": device == "mist" and (reading.humidity > 75 or reading.rain > 25)} for device in node.devices_attached}, "health": {"battery_pct": node.battery_pct, "solar_charging": node.solar_charging, "lora_rssi": node.lora_rssi, "last_seen": node.last_seen, "firmware": node.firmware}}
