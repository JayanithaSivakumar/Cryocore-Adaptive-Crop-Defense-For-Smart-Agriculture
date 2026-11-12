# Python + Spark Intelligence Core

This add-on provides the node registry and per-node intelligence layer for Crop Bodyguard. It is intentionally separate from the existing Vite prototype so the UI can migrate to the Python API incrementally.

## Install and run

```bash
cd python_core
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8790
```

The demo farm is `Coimbatore Demo Farm`, with 12 simulated nodes across 5 zones and 6 crops. The node registry is generated from `crop_bodyguard_core.registry.demo_nodes`, so it remains editable and explicit.

## Endpoints

- `GET /api/farm/summary`
- `GET /api/nodes`
- `GET /api/nodes/{node_id}/overview`
- `GET /api/nodes/{node_id}/history?range=24h&agg=1m`
- `GET /api/nodes/compare?a=CB-05&b=CB-07`
- `POST /api/simulate` with `{ "scenario": "Frost night", "node_ids": ["CB-05", "CB-06"] }`
- `PATCH /api/nodes/CB-09?crop=sunflower`
- `POST /api/nodes/{node_id}/devices/{device}`
- `POST /api/ingest`
- WebSocket `/live`

Frost night targets Zone 3, so CB-05 and CB-06 become danger nodes while other zones retain their own readings. Heat wave targets Zone 4 and drought targets CB-07.

## Spark ETL

```bash
python spark_etl.py
```

With PySpark installed this uses an explicit sensor schema, drops the empty column, trims and lowercases crop data, deduplicates sensor rows, and writes Parquet. Without PySpark it runs a standard-library cleaning fallback into `parquet/*.json`, which makes the data rules testable on a lightweight laptop.

The production extension point is `spark/streaming/`: use Structured Streaming with a two-minute watermark, node-window aggregations, checkpointing, and `foreachBatch` persistence. Rule risk remains available as a deterministic fallback if an MLlib model or optional Scala UDF jar is unavailable.

## Tests

```bash
pytest python_core/tests
```
