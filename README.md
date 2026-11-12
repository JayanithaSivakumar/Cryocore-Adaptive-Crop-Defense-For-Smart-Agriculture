# Crop Bodyguard

Crop Bodyguard is a responsive farmer-facing PWA prototype backed by the supplied sensor, farm, yield, and district climate datasets. It is designed around icon-first status, voice feedback, large touch targets, and a demo path that can be shown without hardware.

## Run locally

```bash
npm install
npm run dev
```

Open http://localhost:5173. The Vite app proxies `/api` to the Express simulator on port 8787. To run only the API, use `npm run server`.

The setup copies the four source CSVs into `data/`. The 76 MB climate dataset stays server-side; the browser only receives aggregate/profile responses.

## Demo path

1. Open the Farm screen and tap `Frost night` under Demo Simulator.
2. Zone 3 changes to 2.5 °C with high humidity; the risk card and alert timeline update.
3. Use the speaker button to hear the alert.
4. Open Control, switch on the Zone 3 heater, then return to Alerts and acknowledge it.
5. Try Heat wave, Drought, Heavy rain, and All clear to exercise the alarm language.

## API boundary

Implemented routes include `/api/zones`, `/api/zones/:id/history`, `/api/alerts`, `/api/alerts/:id/ack`, `/api/devices/:zone/:device`, `/api/simulate`, `/api/crop-profile`, `/api/insights/yield`, `/api/risk`, `/api/farms/demo`, `/api/push/subscribe`, `/api/ingest`, and the SSE stream `/live`.

`server/index.mjs` owns CSV loading and the simulator risk engine. Replace that adapter with a LoRa/MQTT implementation without changing the React UI contract.

## Notes

- Voice uses the browser Web Speech API and requires a user gesture in browsers that block autoplay.
- The service worker caches the shell and intentionally leaves API requests network-first for fresh readings.
- Push, SMS, WhatsApp, and ML training are integration boundaries in this prototype; the climate route already exposes the ideal threshold fields needed to connect a trained risk model.
# Cryocore---Adaptive-Crop-Defense-For-Smart-Agriculture
# Cryocore---Adaptive-Crop-Defense-For-Smart-Agriculture
