# GraphMind AI — Deployment Guide

## Services
| Service | Platform | Directory |
|---|---|---|
| Frontend (Next.js) | Vercel | `frontend/` |
| Backend (FastAPI) | Render | `backend/` |
| Graph Database | Neo4j AuraDB | Managed cloud |
| File Storage | Cloudflare R2 | Managed cloud |
| Auth | Firebase | Managed cloud |

---

## Step 1 — Neo4j AuraDB

1. Go to [console.neo4j.io](https://console.neo4j.io) and sign up / log in.
2. Click **New Instance** → choose **AuraDB Free**.
3. Download the generated credentials file — it contains your URI, username, and password.
4. Your URI will look like: `neo4j+s://xxxxxxxx.databases.neo4j.io`
5. Save these for the Render env vars step.

---

## Step 2 — Cloudflare R2

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → **R2 Object Storage**.
2. Click **Create bucket** → name it `graphmind-uploads`.
3. Go to **R2 → Manage R2 API Tokens** → **Create API Token**.
   - Permissions: **Object Read & Write**
   - Scope: the `graphmind-uploads` bucket
4. Copy the **Access Key ID** and **Secret Access Key**.
5. Your **Account ID** is shown on the R2 overview page (top right).
6. (Optional) Enable **Public Access** on the bucket to get a `pub-xxxx.r2.dev` URL.

---

## Step 3 — Firebase Service Account

1. Go to [Firebase Console](https://console.firebase.google.com) → your project.
2. **Project Settings** → **Service Accounts** → **Generate new private key**.
3. Download the JSON file.
4. For Render, you'll paste the entire JSON as a single-line string in `FIREBASE_SERVICE_ACCOUNT_JSON`.
   - On Linux/Mac: `cat serviceAccountKey.json | tr -d '\n'`
   - On Windows PowerShell: `(Get-Content serviceAccountKey.json -Raw) -replace '\s',''`

---

## Step 4 — Deploy Backend to Render

1. Push this repo to GitHub (if not already).
2. Go to [render.com](https://render.com) → **New** → **Web Service**.
3. Connect your GitHub repo.
4. Render will auto-detect `render.yaml` — confirm the settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add the following **Environment Variables** in the Render dashboard:

```
ALLOWED_ORIGINS=https://your-app.vercel.app
FIREBASE_PROJECT_ID=graphmindai-573e7
FIREBASE_SERVICE_ACCOUNT_JSON=<paste single-line JSON here>
NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=<from AuraDB credentials>
CLOUDFLARE_ACCOUNT_ID=<your account ID>
CLOUDFLARE_R2_ACCESS_KEY_ID=<your R2 access key>
CLOUDFLARE_R2_SECRET_ACCESS_KEY=<your R2 secret>
CLOUDFLARE_R2_BUCKET_NAME=graphmind-uploads
CLOUDFLARE_R2_PUBLIC_URL=https://pub-xxxx.r2.dev
WATSONX_API_KEY=<your key>
WATSONX_PROJECT_ID=<your project ID>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
DEBUG=False
```

6. Click **Deploy**. Once live, copy your Render URL (e.g. `https://graphmind-ai-backend.onrender.com`).

---

## Step 5 — Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**.
2. Import your GitHub repo.
3. Vercel will detect `vercel.json` and set `frontend/` as the root.
4. Add these **Environment Variables** in the Vercel dashboard:

```
NEXT_PUBLIC_API_URL=https://graphmind-ai-backend.onrender.com
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyD2pILHbhzpi35SEM5lz2H4P1HDOvaZrIE
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=graphmindai-573e7.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=graphmindai-573e7
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=graphmindai-573e7.firebasestorage.app
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=1035843137570
NEXT_PUBLIC_FIREBASE_APP_ID=1:1035843137570:web:996f5e1a8541a30c2fda7b
```

5. Click **Deploy**.
6. Once live, copy your Vercel URL (e.g. `https://graphmind-ai.vercel.app`).

---

## Step 6 — Update CORS on Render

After Vercel deploys, go back to Render → your backend service → **Environment** and update:

```
ALLOWED_ORIGINS=https://graphmind-ai.vercel.app
```

Then trigger a **Manual Deploy** on Render to apply the change.

---

## Step 7 — Update vercel.json (optional)

Update `vercel.json` with your actual Render URL:

```json
"env": {
  "NEXT_PUBLIC_API_URL": "https://graphmind-ai-backend.onrender.com"
}
```

---

## Verification Checklist

- [ ] `https://your-backend.onrender.com/health` returns `{"status":"healthy"}`
- [ ] `https://your-backend.onrender.com/docs` shows the FastAPI Swagger UI
- [ ] Frontend loads at your Vercel URL
- [ ] Login / Firebase Auth works
- [ ] Graph loads from the backend
- [ ] Repository upload stores file in R2 bucket
- [ ] Neo4j graph data persists across requests
