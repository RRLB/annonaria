# Annonaria Campaign Platform

A fullstack Ad Tech application to manage advertising campaigns, built with Flask (backend) and Vue.js (frontend), running in Docker.

## 🚀 Features

- CRUD operations for campaigns (name, description, start/end dates, budget, status).
- JWT authentication for secure API access.
- Swagger API documentation (`/apidocs`).
- Responsive Vue.js frontend with Bootstrap in subtle tones.
- Unit tests for backend (pytest) and frontend (Vitest).
- CI/CD with GitHub Actions.

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RRLB/annonaria.git
   cd annonaria
   ```

2. (Optional) If running the frontend outside Docker:

   ```bash
   cd frontend
   npm install
   ```

## 🐳 Running with Docker

1. Set up environment variables:

   ```bash
   cp backend/.env.example backend/.env
   ```

   Then edit the `.env` file (example for SQLite):

   ```ini
   DATABASE_URL=sqlite:///campaigns.   ```

2. Build and run the containers:

   ```bash
   docker-compose up -d --build
   ```

   - Backend: http://localhost:4000/apidocs  
   - Frontend: http://localhost:5173

## 🔐 Test Credentials

- **Username:** `user1`  
- **Password:** `password123`

## 🧪 Running Tests

**Backend:**

```bash
docker exec -it annonariapp pytest tests/
```

**Frontend:**

```bash
docker exec -it annonaria-frontend npm run test
```

## ⚙️ CI/CD

GitHub Actions is used for CI/CD.  
Workflow file: `.github/workflows/ci.yml`

It performs:

- Docker image builds  
- Unit test execution for both frontend and backend

## 🧱 Tech Stack

- **Backend:** Flask, SQLAlchemy, Marshmallow, flask-jwt-extended, Flasgger  
- **Frontend:** Vue 3 (Composition API), Bootstrap 5, axios  
- **Testing:**  
  - Backend: `pytest`  
  - Frontend: `Vitest`  
- **CI/CD:** GitHub Actions  
- **Containerization:** Docker, Docker Compose

## 🔮 Potential Improvements

- Add integration and end-to-end tests  
- Implement JWT refresh token support  
- Paginate campaign list for better UX  
- Set up staging and production deployment pipelines

## 📄 License

MIT License — see `LICENSE` file for details.
