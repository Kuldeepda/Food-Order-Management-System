# 🍽️ Food Ordering System - Python + MySQL CLI App

A simple command-line application to manage customers and food orders using Python and MySQL.  
Users can create accounts, place orders, and view/update orders in a clean CLI interface.

---

## 📦 Features

- Create customer accounts
- Log in using account number
- Place food orders
- View and update existing orders
- Data stored in MySQL using two tables: `myc` (customers) and `sales` (orders)

---

## 🛠️ Requirements

Make sure the following tools are installed on your system:

| Tool         | Version (Recommended) | Installation Link                         |
|--------------|------------------------|-------------------------------------------|
| Python       | 3.11+                  | https://www.python.org/downloads/         |
| MySQL Server | 8.0+                   | https://dev.mysql.com/downloads/installer/ |
| XAMPP        | Optional (GUI for MySQL) | https://www.apachefriends.org/index.html |

---

## 🧰 Required Python Libraries

Only one external library is required:

```bash
pip install mysql-connector-python
