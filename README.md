# Ecommerce Application

## Setup & Installation

### 1. Start the Application
To build and run the application using Docker, execute:
```sh
docker-compose up --build
```

### 2. Apply Database Migrations
After the containers are running, apply database migrations using Alembic:
```sh
docker exec -it app alembic upgrade head
```

### 3. Load Initial Data
To load initial data into PostgreSQL, run:
```sh
docker exec -i ecommerce_postgres psql -U postgres -d postgres < init.sql
```

### 4. Restart the Application
After migrations and data loading, restart the application:
```sh
docker-compose down
docker-compose up
```

## API Endpoints

### **1. Create an Order**
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/order/create_order' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 2,
  "item_ids": [
    12, 3
  ],
  "total_amount": 55.0
}'
```

### **2. Get an Order by ID**
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/order/get_order/2' \
  -H 'accept: application/json'
```

### **3. Get Application Metrics**
```sh
curl -X 'GET' \
  'http://localhost:8000/metrics' \
  -H 'accept: application/json'
```


### **Accessing FastAPI Docs**
If `http://localhost:8000/docs` is not working, make sure `main.py` is updated with:

