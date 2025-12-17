# PictureBoard Documentation

## 1. Overview
PictureBoard is a real-time, auto-scrolling photo memory board application designed for events (weddings, parties, conferences). Guests upload photos via a mobile web interface (no app required), and the photos instantly appear on a large screen display in a beautiful masonry layout.

## 2. Architecture

### 2.1 Technology Stack
*   **Backend**: Python (Flask)
    *   **Database**: PostgreSQL (Data persistence)
    *   **ORM**: SQLAlchemy
    *   **Async Tasks**: Celery + Redis (Image processing queue)
    *   **Real-time**: Flask-SocketIO (WebSocket communication)
*   **Frontend**: Vue.js 3 (Vite)
    *   **Styling**: TailwindCSS
    *   **Routing**: Vue Router
    *   **State**: Composition API
*   **Infrastructure**: Docker & Docker Compose

### 2.2 System Flow
1.  **Host** registers and creates a "Board" (Event).
2.  **Host** opens the "Board Viewer" on a large screen (projector/TV).
3.  **Host** shares a QR Code with **Guests**.
4.  **Guests** scan the QR code to open the "Upload Page" on their phones.
5.  **Guests** upload photos.
6.  **Backend** saves the photo and emits a `new_photo` Socket.IO event.
7.  **Board Viewer** receives the event and appends the photo to the grid in real-time.

## 3. Directory Structure

```text
/
├── services/
│   ├── backend/         # Flask API
│   │   ├── src/
│   │   │   ├── api/     # Route definitions (Blueprint)
│   │   │   ├── models/  # Database Models (User, Board, Photo)
│   │   │   ├── static/  # Uploaded images (Local dev storage)
│   │   │   └── ...
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── client/          # Vue.js SPA
│   │   ├── src/
│   │   │   ├── views/   # Page components
│   │   │   ├── router/  # Navigation logic
│   │   │   └── ...
│   │   ├── Dockerfile
│   │   └── package.json
├── docker-compose.yml   # Orchestration
└── PLAN.md              # Original Development Plan
```

## 4. API Reference

### 4.1 Authentication
*   `POST /auth/register`: Create a new user account.
*   `POST /auth/login`: Authenticate and receive a JWT.
*   `GET /auth/status`: Verify current token validity.

### 4.2 Boards
*   `GET /boards`: List all boards for the logged-in user.
*   `POST /boards`: Create a new board.
    *   Payload: `{ "title": "My Event", "slug": "my-event" }`
*   `GET /boards/<id>`: Get board details.
*   `PUT /boards/<id>`: Update board settings.

### 4.3 Uploads
*   `POST /upload/<slug>`: Public endpoint for uploading photos.
    *   Form Data: `file` (Image)
    *   Response: JSON with photo URL.
    *   **Side Effect**: Emits `new_photo` socket event to room `<slug>`.

### 4.4 Viewer
*   `GET /view/<slug>`: Public endpoint to fetch initial board state (Settings + Existing Photos).

## 5. Deployment & Setup

### 5.1 Prerequisites
*   Docker and Docker Compose installed.

### 5.2 Local Development
1.  **Build and Start**:
    ```bash
    docker compose up -d --build
    ```
2.  **Initialize Database** (First time only):
    ```bash
    docker compose exec backend python manage.py recreate_db
    ```
3.  **Access the App**:
    *   Frontend: `http://localhost:5173`
    *   Backend API: `http://localhost:5001`

### 5.3 Usage Guide
1.  Go to `http://localhost:5173`.
2.  **Register** a new account.
3.  **Login** to access the Dashboard.
4.  **Create a Board** with a unique "Slug" (e.g., `wedding-2024`).
5.  Click **Settings** on the board card.
6.  **Display**: Open the "Board Viewer" link on your main display.
7.  **Upload**: Scan the QR code with your phone to upload test photos.

## 6. Future Improvements (Roadmap)
*   **Production Storage**: Replace local file storage with AWS S3 or Google Cloud Storage.
*   **Image Optimization**: Implement the Celery task to resize/compress images in the background.
*   **Moderation**: Add an "Approve/Reject" flow for hosts before photos go live.
*   **Animation Modes**: Implement "Ken Burns" slideshow and other complex visualizers using GSAP.
