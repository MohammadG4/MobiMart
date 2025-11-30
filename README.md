# MobiMart

A modular, mobile ecommerce backend built with **Django** and **Django REST Framework** (DRF) frontend built with **Next.js** database with **PostgreSQL**. MobiMart is designed for scalability, clean architecture, and maintainability — suitable for mobile apps or SPA front‑ends.

---

## 🚀 Features

### **Core Functionality**

* User authentication (JWT-based)
* Profiles & custom user model
* Product catalog with categories, brands, variations
* Shopping cart with coupon support
* Orders, payments, and statuses
* Wishlist / favorites
* Reviews & ratings
* Address management
* Search & filtering
* Admin dashboard controls

### **Technical Features**

* REST API built with DRF
* Token auth using SimpleJWT
* Custom permissions & throttling
* Pagination and filtering
* Signals for order events & inventory updates
* Modular app structure for scalability
* Docker-ready 

---

## 🧱 Project Structure (Recommended)

```
mobimart/
├── config/               # Django project settings
├── users/                # Custom user model, auth, JWT endpoints
├── products/             # Products, categories, brands, reviews
├── cart/                 # Shopping cart, coupons
├── orders/               # Orders, payments, statuses
├── addresses/            # User addresses
├── wishlist/             # Wishlist / favorites
├── utils/                # Helpers, common utilities
└── requirements.txt
```

### Why this structure?

* Keeps apps isolated and reusable
* Makes testing easier
* Makes scaling the project easier (microservices ready)

---

## ⚙️ Installation

### 1. Clone the repo

```
git clone https://github.com/yourname/mobimart.git
cd mobimart
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Apply migrations

```
python manage.py migrate
```

### 5. Create superuser

```
python manage.py createsuperuser
```

### 6. Run development server

```
python manage.py runserver
```

---

## 🔐 Authentication

MobiMart uses **JWT via SimpleJWT**.

### Endpoints

* `POST /api/auth/login/`
* `POST /api/auth/register/`
* `POST /api/auth/token/refresh/`
* `POST /api/auth/logout/` (blacklists tokens)

### Storage

* Access token stored in memory (mobile)
* Refresh token stored in HttpOnly cookie

---

## 🛍️ Apps Overview

### **Users App**

* CustomUser model
* JWT authentication
* Permissions (IsAdmin, IsOwner)
* Profile endpoints

### **Products App**

* Categories
* Brands
* Product variations & attributes
* Inventory system
* Reviews (with restrictions: only purchased users)

### **Cart App**

* Add / remove items
* Auto-update quantities
* Coupons
* Calculates totals dynamically

### **Orders App**

* Order creation
* Payment integration ready (Cash on Delivery)
* Signals to update inventory after payment
* Order tracking statuses

### **Wishlist App**

* Add/remove favorites
* Linked to product

---

## 📡 API Examples

### Add to Cart

```
POST /api/cart/add/
{
  "product_id": 1,
  "quantity": 2
}
```

### Apply Coupon

```
POST /api/cart/apply-coupon/
{
  "code": "DISCOUNT10"
}
```

### Create Order

```
POST /api/orders/create/
{
  "address_id": 3
}
```

---

## 🧪 Testing

```
pytest
```

Automatically discovers tests per app.

---

## 📦 Deployment Notes

### Environment variables required

```
SECRET_KEY=
DEBUG=False
DATABASE_URL=
ALLOWED_HOSTS=
JWT_SECRET=
```

### Docker Support (Optional)

```
docker-compose up --build
```

---

## 🔧 Future Enhancements

* Multi-vendor support
* Product recommendations (ML-ready)
* Notifications (email, SMS)
* Payment gateway integrations
* Analytics dashboards

---

## 📄 License

MIT License

---

## 👤 Author

**Mohammad Gafour**
**Nour Elmaghraby**

* Backend: Django + DRF
* Frontend: Next.js + TailwindCSS
* Architecture: Modular Clean Design


