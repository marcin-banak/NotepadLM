#!/bin/bash

# ==============================
# Skrypt uruchamia backend + frontend
# ==============================

# Zatrzymanie przy błędach
set -e

# ==============================
# Aktywacja środowiska wirtualnego
# ==============================
if [ -z "$VIRTUAL_ENV" ]; then
  if [ -f ".venv/bin/activate" ]; then
    echo "Aktywuję środowisko wirtualne .venv..."
    source .venv/bin/activate
  else
    echo "Nie znaleziono środowiska .venv. Utwórz je poleceniem 'pdm install'"
    exit 1
  fi
else
  echo "Środowisko wirtualne już aktywne: $VIRTUAL_ENV"
fi

# ==============================
# Załaduj zmienne środowiskowe
# ==============================
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  echo "Załadowano zmienne z .env"
else
  echo "Nie znaleziono pliku .env, kontynuuję..."
fi

# ==============================
# Funkcja do uruchomienia backendu
# ==============================
start_backend() {
  echo "Uruchamianie backendu FastAPI..."
  uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload --app-dir src &
  BACKEND_PID=$!
  echo "Backend PID: $BACKEND_PID"
}

# ==============================
# Funkcja do uruchomienia frontendu
# ==============================
start_frontend() {
  echo "Uruchamianie frontendu Vite..."
  npm --prefix src/frontend run dev &
  FRONTEND_PID=$!
  echo "Frontend PID: $FRONTEND_PID"
}

# ==============================
# Uruchom oba serwisy
# ==============================
start_backend
start_frontend

# ==============================
# Funkcja do czyszczenia po Ctrl+C
# ==============================
cleanup() {
  echo "Zatrzymywanie procesów..."
  kill $BACKEND_PID $FRONTEND_PID
  exit 0
}

trap cleanup SIGINT SIGTERM

# Czekaj na oba procesy
wait $BACKEND_PID
wait $FRONTEND_PID
