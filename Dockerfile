# --- Stage 1: Build the React/Vite Frontend ---
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
# Use your exact folder name 'lms_frontend'
COPY lms_frontend/package*.json ./
RUN npm install
COPY lms_frontend/ ./
RUN npm run build

# Stage 2: Setup the Django Backend
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY lms_backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY lms_backend/ ./
COPY --from=frontend-build /app/frontend/dist ./static_dist

# --- UPDATED FOR PORT 3000 ---
EXPOSE 3000
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
