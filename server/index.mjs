import express from 'express'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import Papa from 'papaparse'

const root = path.dirname(fileURLToPath(import.meta.url))
const dataDir = path.join(root, '..', 'data')
const readCsv = (name) => Papa.parse(fs.readFileSync(path.join(dataDir, name), 'utf8'), { header: true, dynamicTyping: true, skipEmptyLines: true }).data
const sensorRows = readCsv('Dataset_sensors.csv')
const farms = readCsv('agriculture_dataset.csv')
const yields = readCsv('crop_yield.csv')
const zones = ['North Orchard', 'River Edge', 'Tomato Patch', 'Seed House', 'East Field']
let scenario = 'All clear'
let tick = 0
let alerts = []
let deviceStates = {}

const baseReading = () => {
  const row = sensorRows[tick % sensorRows.length]
  const values = { temperature: Number(row.weather_temperature), humidity: Number(row.weather_humidity), solar: Number(row.solar_radiation), moisture: Number(row.soil_moisture), soilTemperature: Number(row.soil_temperature), rain: 0, wind: 2.8 }
  return values
}
const statusFor = (reading, index) => {
  const variant = { ...reading, temperature: reading.temperature + (index - 2) * 1.4, moisture: reading.moisture - Math.max(0, index - 2) * 3 }
  if (scenario === 'Frost night' && index === 2) Object.assign(variant, { temperature: 2.5, humidity: 95 })
  if (scenario === 'Heat wave' && index === 3) Object.assign(variant, { temperature: 42, humidity: 25 })
  if (scenario === 'Drought' && index === 4) Object.assign(variant, { moisture: 12, temperature: 34, humidity: 31 })
  if (scenario === 'Heavy rain' && index === 1) Object.assign(variant, { rain: 48, humidity: 93, solar: 8, temperature: 25 })
  const danger = variant.temperature <= 4 ? ['DANGER', 'Frost', '❄️', 91] : variant.temperature >= 38 ? ['DANGER', 'Heat', '☀️', 87] : variant.moisture < 20 ? ['DANGER', 'Drought', '💧', 82] : variant.rain > 35 ? ['DANGER', 'Heavy rain', '🌧️', 88] : variant.temperature < 8 || variant.moisture < 30 ? ['WATCH', 'Check conditions', '◌', 45] : ['SAFE', 'All clear', '✓', 8]
  return { id: index + 1, name: zones[index], ...variant, status: danger[0], hazard: danger[1], icon: danger[2], risk: danger[3], battery: 78 - index * 4, signal: 4 - (index % 2), updated: new Date().toISOString() }
}
const zoneList = () => zones.map((_, index) => statusFor(baseReading(), index))

const app = express()
app.use(express.json())
app.get('/api/zones', (_, res) => { tick++; res.json(zoneList()) })
app.get('/api/zones/:id/history', (req, res) => {
  const current = statusFor(baseReading(), Number(req.params.id) - 1)
  res.json(Array.from({ length: 12 }, (_, index) => ({ time: `${12 + index}:00`, temperature: +(current.temperature + Math.sin(index / 2) * 2).toFixed(1), moisture: +(current.moisture + Math.cos(index / 3) * 3).toFixed(1) })))
})
app.get('/api/alerts', (_, res) => res.json(alerts))
app.post('/api/alerts/:id/ack', (req, res) => { alerts = alerts.map((alert) => alert.id === req.params.id ? { ...alert, acknowledged: true } : alert); res.json({ ok: true }) })
app.post('/api/devices/:zone/:device', (req, res) => { const key = `${req.params.zone}-${req.params.device}`; deviceStates[key] = req.body.state; res.json({ ok: true, key, state: req.body.state }) })
app.post('/api/simulate', (req, res) => { scenario = req.body.scenario || 'All clear'; const zonesNow = zoneList(); const danger = zonesNow.find((zone) => zone.status === 'DANGER'); if (danger) alerts.unshift({ id: `${Date.now()}`, zone: danger.name, type: danger.hazard, icon: danger.icon, severity: danger.status, time: new Date().toISOString(), message: `${danger.hazard} danger in ${danger.name}.`, acknowledged: false }); res.json({ scenario, zones: zonesNow }) })
app.get('/api/farms/demo', (_, res) => res.json(farms.slice(0, 5)))
app.get('/api/insights/yield', (req, res) => { const crop = String(req.query.crop || 'Rice').toLowerCase(); const state = String(req.query.state || 'Tamil Nadu').toLowerCase(); const rows = yields.filter((row) => String(row.crop).trim().toLowerCase().includes(crop) && String(row.state).trim().toLowerCase() === state).slice(-8); res.json(rows.length ? rows : yields.slice(0, 8)) })
app.get('/api/crop-profile', (_, res) => res.json({ crop: 'Rice', state: 'Tamil Nadu', district: 'Thanjavur', Tmin_Ideal: 20, Tmax_Ideal: 35, Rain_Ideal: 8, RH_Ideal: 70, criticalRate: 18, topCause: 'Heat deviation' }))
app.get('/api/risk', (_, res) => res.json({ risk: scenario === 'All clear' ? 8 : 91, outlook: [8, 12, 18, 32, 44, 38, 22] }))
app.get('/live', (_, res) => {
  res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' })
  const timer = setInterval(() => res.write(`data: ${JSON.stringify(zoneList())}\n\n`), 5000)
  res.on('close', () => clearInterval(timer))
})
app.post('/api/push/subscribe', (req, res) => res.status(202).json({ ok: true, queued: Boolean(req.body) }))
app.post('/api/ingest', (req, res) => res.status(202).json({ ok: true, message: 'Packet accepted for the simulator gateway boundary.', packet: req.body }))
app.listen(process.env.PORT || 8787, () => console.log('Crop Bodyguard API on 8787'))
