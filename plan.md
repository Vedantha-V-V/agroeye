# AgroEye

## 1. Owners
| Owner | Role | Scope |
|---|---|---|
| A | AI / Inference | Model, eval, inference service, health maps |
| B | Backend / Infra | API, DB, storage, auth, hosting, CI |
| C | Frontend / UX | React app, map UI, charts, deploy |

## 2. Open decisions
- [ ] Ingest mode: batch upload only, or batch + live stream? (Rec: batch first, live = stretch)
- [ ] Hosting target for backend (CPU inference needed; no GPU)
- [ ] DB: PostgreSQL vs SQLite
- [ ] Auth: needed for demo? (Rec: simple email/JWT or skip)
- [ ] Map lib: Leaflet vs Mapbox
- [ ] Extend JSON contract: add `lat`, `lon`, `field_id`, `flight_id`

## 3. Phase 1 — Foundation
- [ ] Repo setup: monorepo `/frontend`, `/backend`, `/ml`, `/docs` (B)
- [ ] API contract v2 agreed, OpenAPI spec frozen (A+B+C)
- [ ] Mock API with fake JSON so frontend unblocked (B)
- [ ] React scaffold + routing + UI kit (C)
- [ ] Confirm `finetuned_model` loads in standalone script (A)
- [ ] Notion board + weekly sync (all)

## 4. Phase 2 — Core build (parallel)

### A — AI / Inference
- [ ] Wire `finetuned_model` into `main.py` (`MODEL_NAME`)
- [ ] Run final `evaluate.py`, record metrics
- [ ] Inference service: image → JSON contract
- [ ] Batch processing for flight folder
- [ ] Health score + anomaly flags logic
- [ ] Grid / heatmap generation from geo-tagged results
- [ ] Delete deprecated `wambugu71` model + `model_cache`

### B — Backend / Infra
- [ ] FastAPI endpoints: `/health`, `/upload`, `/infer`, `/flights`, `/flights/{id}/results`
- [ ] Image storage (local disk or S3-compatible)
- [ ] DB schema: users, fields, flights, images, results
- [ ] Async job queue for batch inference (BackgroundTasks first, Celery if time)
- [ ] EXIF GPS extraction from drone images
- [ ] CORS, validation, error handling
- [ ] Dockerfile + docker-compose

### C — Frontend
- [ ] Upload page (drag-drop, progress)
- [ ] Dashboard: flight list, status
- [ ] Map view: field overlay, health heatmap, markers
- [ ] Image detail: disease, confidence, `frame_base64`/image preview
- [ ] Charts: health score trend, disease distribution
- [ ] Insights panel: action recommendations
- [ ] Responsive layout (farmers use phones via browser)

## 5. Phase 3 — Integrate
- [ ] Swap mock API for real API (C+B)
- [ ] End-to-end test: upload → inference → map (all)
- [ ] Fix contract mismatches
- [ ] Performance check: time per image, batch size limits (A)
- [ ] Error states + empty states in UI (C)

## 6. Phase 4 — Host + Ship
- [ ] Frontend deploy: Vercel / Netlify (C)
- [ ] Backend deploy: Render / Railway / Fly.io / lab PC + tunnel (B)
- [ ] Env vars, secrets, HTTPS (B)
- [ ] Model weights delivery to host (A+B)
- [ ] Smoke test on live URL (all)
- [ ] CI: lint + tests on PR (B)

## 7. Phase 5 — Review prep
- [ ] Demo dataset + scripted demo flow
- [ ] Architecture diagram (Mermaid)
- [ ] README + run instructions
- [ ] Slides, metrics, limitations
- [ ] Dry run