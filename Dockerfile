# Stage 1: Build the Angular app
FROM node:16 AS frontend-build

WORKDIR /app

# Copy package.json and package-lock.json files
COPY frontend/package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ .

# Build the Angular app
RUN npm run build --prod

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py
COPY static/ static/
# Copy the built Angular app from the frontend-build stage
COPY --from=frontend-build /app/dist/frontend /app/static/

EXPOSE 8080

# Set the entry point to start the backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
