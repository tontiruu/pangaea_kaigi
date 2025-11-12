.PHONY: start stop install-backend install-frontend install dev-backend dev-frontend

# Start both frontend and backend
start:
	@echo "Starting backend and frontend..."
	@make -j 2 dev-backend dev-frontend

# Stop all running processes
stop:
	@echo "Stopping all processes..."
	@pkill -f "uvicorn" || true
	@pkill -f "next dev" || true

# Install backend dependencies
install-backend:
	@echo "Installing backend dependencies..."
	cd backend && pip3 install -r requirements.txt

# Install frontend dependencies
install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Install all dependencies
install: install-backend install-frontend

# Run backend development server
dev-backend:
	@echo "Starting FastAPI backend..."
	cd backend && python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run frontend development server
dev-frontend:
	@echo "Starting Next.js frontend..."
	cd frontend && npm run dev
