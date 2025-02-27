# 🚗 Ride-Sharing API 🚀  

Welcome to the **Ride-Sharing API**! This API powers a seamless ride-hailing experience—where riders request rides, drivers accept them, and real-time updates keep everything in motion.  

---

## 📌 Features  

✅ **User Authentication** (Register/Login)  
✅ **Ride Requests** (Riders book trips)  
✅ **Driver Matching** (Assign drivers to rides)  
✅ **Ride Acceptance** (Drivers confirm rides)  
✅ **Real-time Location Updates** (Driver movement tracking)  
✅ **Ride Status Updates** (In-progress, Completed, etc.)  
✅ **View Rides** (Retrieve ride history)  

---

## ⚙️ Setup Instructions  

### 🛠️ Prerequisites  

- **Python 3.x**  
- **Django & Django REST Framework**  
- **Postman** (For API Testing)  

### 🔧 Installation Steps  

#### 1️⃣ Clone the Repository  

```sh
git clone https://github.com/Amitha95/ride-sharing-api.git
cd ride-sharing-api

```

### 2️⃣ Set Up a Virtual Environment  

```sh
python -m venv venv
```

#### Activate it:  

- **Windows**  
  ```sh
  venv\Scripts\activate
  ```

- **Mac/Linux**  
  ```sh
  source venv/bin/activate
  ```

### 3️⃣ Install Dependencies  

```sh
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations  

```sh
python manage.py migrate
```

### 5️⃣ Run the Development Server  

```sh
python manage.py runserver
```

Your API should now be accessible at:  
[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) 🚀  

---

## 🔥 API Endpoints  

### 🧑‍💻 1️⃣ User Registration  
**Endpoint:**  
```http
POST /api/users/register/
```
**Request Body (JSON):**  
```json
{
  "username": "testuser",
  "password": "password123",
  "email": "testuser@example.com",
  "role": "rider"
}
```
**Response:** `201 Created`  

---

### 🔐 2️⃣ User Login  
**Endpoint:**  
```http
POST /api/users/login/
```
**Request Body (JSON):**  
```json
{
  "username": "testuser",
  "password": "password123"
}
```
**Response:** `200 OK`  

---

### 🚖 3️⃣ Request a Ride  
**Endpoint:**  
```http
POST /api/rides/
```
**Headers:**  
```
Authorization: Bearer <token>
```
**Request Body (JSON):**  
```json
{
  "pickup_location": "Location A",
  "dropoff_location": "Location B"
}
```
**Response:** `201 Created`  

---

### 🚙 4️⃣ Match Ride to Driver  
**Endpoint:**  
```http
POST /api/rides/match_ride/
```
**Headers:**  
```
Authorization: Bearer <token>
```
**Request Body (JSON):**  
```json
{
  "ride_id": 1,
  "driver_id": 2
}
```
**Response:** `200 OK`  

---

### 👨‍✈️ 5️⃣ Driver Accepts Ride  
**Endpoint:**  
```http
POST /api/rides/{id}/accept_ride/
```
**Headers:**  
```
Authorization: Bearer <token>
```
**Request Body (JSON):**  
```json
{
  "driver_id": 2
}
```
**Response:** `200 OK`  

---

### 📍 6️⃣ Driver Updates Location  
**Endpoint:**  
```http
PATCH /api/rides/{id}/update_location/
```
**Headers:**  
```
Authorization: Bearer <token>
```
**Request Body (JSON):**  
```json
{
  "latitude": 37.7749,
  "longitude": -122.4194
}
```
**Response:** `200 OK`  

---

### 🔄 7️⃣ Update Ride Status  
**Endpoint:**  
```http
PATCH /api/rides/{id}/update_status/
```
**Headers:**  
```
Authorization: Bearer <token>
```
**Request Body (JSON):**  
```json
{
  "status": "completed"
}
```
**Response:** `200 OK`  

---

### 📜 8️⃣ Get All Rides  
**Endpoint:**  
```http
GET /api/rides/
```
**Headers:**  
```
Authorization: Bearer <token>
```
**Response:** `200 OK`  

---

## 🧪 Testing the API with Postman  

### 🚀 Follow these steps to test the API in Postman:  

1️⃣ **Register a new user** *(Rider registers first)*  
2️⃣ **Log in & obtain the access token**  
3️⃣ **Use the token in the Authorization header for all requests**  
4️⃣ **Follow the API flow:**  

```
Rider registers and logs in  
→ Requests a ride  
→ Admin matches a driver to the ride  
→ Driver registers and logs in  
→ Driver accepts the ride  
→ Driver updates their location  
→ Ride status updates (e.g., In Progress → Completed)  
→ View ride history  
```

---

## 🧪 Testing  

1️⃣ Ride Matching Algorithm Test

Matches a driver to a ride via POST /api/rides/match_ride/

2️⃣ Driver Accepting Ride Test

Driver accepts a ride via POST /api/rides/{id}/accept_ride/

3️⃣ Driver Location Updates Test

Simulates a driver updating their location via PATCH /api/rides/{id}/update_location/

4️⃣ Ride Status Update Test

Ensures ride status transitions correctly (e.g., "completed")

5️⃣ Ride Tracking Simulation Test

Simulates multiple location updates during a ride
```
