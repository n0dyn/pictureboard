# Auto-Scrolling Photo Memory Application - Development Plan

## 1. Project Overview
A multi-tenant, real-time photo memory board application. Users (Hosts) create "Boards" (Events). Guests scan a QR code to upload photos via a mobile-optimized web interface. Photos appear in real-time on a "Board" displayed on a large screen/projector, utilizing various auto-scrolling animation modes.

## 2. Tech Stack
-   **Backend**: Python 3.11+, Flask, SQLAlchemy, Celery, Redis, Flask-SocketIO.
-   **Database**: PostgreSQL.
-   **Frontend**: Vue.js 3, TailwindCSS, GSAP.
-   **Infrastructure**: Docker, Docker Compose, Nginx.

## 3. Directory Structure
```text
/
├── services/
│   ├── backend/         # Flask API
│   │   ├── src/
│   │   │   ├── api/
│   │   │   ├── models/
│   │   │   ├── services/ # Business logic (S3, Image processing)
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── tasks.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── manage.py
│   ├── client/          # Vue.js SPA
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── ...
│   └── nginx/           # Reverse Proxy
├── docker-compose.yml
└── .env
```

## 4. Implementation Phases

### Phase 1: The Foundation (Boilerplate & Auth)
**Goal**: Functional containerized environment with user authentication.

*   **Step 1.1: Infrastructure Setup**
    *   Create directory structure.
    *   Setup `docker-compose.yml` (Flask, Postgres, Redis, Client placeholder).
*   **Step 1.2: Backend Scaffold**
    *   Initialize Flask app factory.
    *   Setup SQLAlchemy and Migrations (Alembic).
    *   Define `User` model.
*   **Step 1.3: Authentication**
    *   Implement Flask-Bcrypt and PyJWT.
    *   Create endpoints: `/auth/register`, `/auth/login`, `/auth/status`.
*   **Step 1.4: Frontend Setup**
    *   Initialize Vue 3 project (Vite).
    *   Setup TailwindCSS.
    *   Implement Login/Register forms.
    *   Connect to Backend Auth API.

### Phase 2: Board Management (Core Logic)
**Goal**: Users can create and manage event boards.

*   **Step 2.1: Board Model**
    *   Create `Board` model (slug, settings, owner_id).
    *   Relationship: User -> Boards.
*   **Step 2.2: Board API**
    *   CRUD Endpoints: `POST /boards`, `GET /boards`, `PUT /boards/<id>`.
    *   QR Code generation endpoint.
*   **Step 2.3: Dashboard UI**
    *   List view of created boards.
    *   Settings form (Theme, Animation Mode).
    *   QR Code display.

### Phase 3: The "Scanner" (Uploads)
**Goal**: Guest photo uploads via mobile.

*   **Step 3.1: Photo Model & Storage**
    *   Create `Photo` model (filename, url, status).
    *   Setup local file storage (dev) / S3 integration (prod).
*   **Step 3.2: Async Processing (Celery)**
    *   Setup Celery worker.
    *   Task: Resize/Optimize image.
*   **Step 3.3: Public Upload API**
    *   `POST /upload/<board_slug>` (Authorized via token, not user login).
*   **Step 3.4: Mobile Upload UI**
    *   Simple, high-performance upload page.
    *   Client-side image compression.

### Phase 4: The "Memory Board" (Display & Real-time)
**Goal**: The main display visualization.

*   **Step 4.1: Real-time (SocketIO)**
    *   Backend: Emit `new_photo` event on upload completion.
    *   Frontend: Listen for `new_photo` and update state.
*   **Step 4.2: Display Logic**
    *   Create `/view/<slug>` route.
    *   Implement "Masonry" scroll (Virtual Scroller).
    *   Implement "Slideshow" mode.
*   **Step 4.3: Animation Polish**
    *   Integrate GSAP for transitions.

### Phase 5: Polish & Production
*   **Step 5.1: Moderation Queue**.
*   **Step 5.2: Nginx Configuration**.
*   **Step 5.3: Production Build Optimization**.
