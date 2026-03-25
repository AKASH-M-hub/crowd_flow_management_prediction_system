# CogniVue AI Frontend

This frontend is integrated with the Crowd System AI Python modules.

## Module Launcher Integration

The dashboard includes controls to launch and stop these backend modules:

- `main.py` (live detection + prediction)
- `main2.py` (timeline prediction studio)
- `geospatial_dashboard.py` (geospatial intelligence dashboard)

### 1. Start Python launcher API

From the project root:

```powershell
python frontend/module_launcher_api.py
```

By default it runs on `http://127.0.0.1:5001`.

### 2. Start frontend

From `frontend/crowd-sense-ai`:

```powershell
npm install
npm run dev
```

Or run frontend + launcher API together from `frontend/crowd-sense-ai`:

```powershell
npm run dev:full
```

Open the frontend URL printed by Vite (typically `http://127.0.0.1:5173`).

### 3. Use module controls

Go to `/dashboard` and use the **Execution Modules** panel to start/stop modules.

## Optional API URL override

If needed, set a custom backend URL:

```powershell
$env:VITE_CPS_API_URL = "http://127.0.0.1:5001"
```

Then restart the frontend dev server.
