# E-Commerce Site
<img src="https://i.imgur.com/yabCF96.jpeg" alt="E-Commerce Site Logo" width="500">

## About the Project

This is a **Django-based e-commerce platform** that allows users to browse products, add them to their carts, and complete purchases. The system supports user authentication, product reviews, and a seller dashboard.

**This project is actively being developed** and may still contain bugs. If you encounter any issues, feel free to report them.  

## Features

- **User Authentication** – Register, login, and manage accounts  
- **Product Management** – Add, edit, and delete products (admin/seller only)  
- **Shopping Cart & Checkout** – Users can add items to cart and purchase  
- **Review & Ratings** – Customers can leave reviews and rate products  
- **Order History** – Users can track their past purchases  
- **Seller Dashboard** – Sellers can manage their products and see sales statistics  
- **Premium Sellers** – Sellers can upgrade to **premium status** for additional benefits  
- **Admin Panel** – Manage users, products, and orders  

## Technologies Used

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** PostgreSQL
- **Styling:** Tailwind CSS

## Installation

### Clone the repository  
```sh
git clone https://github.com/furkanalk/e-commerce-site.git
cd e-commerce-site
```
### Create and activate a virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Install dependencies
```sh
pip install -r requirements.txt
```
### Apply migrations
```sh
python manage.py migrate
```
### Run the development server
```sh
python manage.py runserver
```

Now, open http://127.0.0.1:8000/ in your browser! 