# Smart-Stock Retail Management System

A backend-focused inventory and sales management system designed for **QuickCart**, a mid-sized retail chain.

This system manages products, processes sales transactions, automates low-stock alerts, and ensures efficient data handling for high-volume stores.

---

## Key Highlights

- O(1) Product Lookup using Dictionary (Hash Map)

- Clean Layered Architecture (Models → Repositories → Business Logic)

- Proper Encapsulation of stock management

- Transactional Sale Processing with custom exception handling

- Automated Low-Stock Detection

- Sorting by Price & Stock

- SQLite-based relational schema with foreign key integrity

- PEP 8 compliant, clean, modular code

---

## Features

- Add, update, delete products
- Increase stock independently
- Process sales transactions with validation
- Preview sale amount before confirmation
- Automatic low-stock detection
- View all sales or filter sales by product
- Sort inventory by price or stock quantity
- Timezone-aware sales timestamps

---

## Database Schema

### Products
| Column         | Type     | Constraints              |
|---------------|----------|--------------------------|
| id            | INTEGER  | Primary Key, Auto Increment |
| name          | TEXT     | NOT NULL                 |
| price         | REAL     | > 0                      |
| stock_quantity| INTEGER  | >= 0                     |

### SalesLog
| Column        | Type     | Constraints              |
|--------------|----------|--------------------------|
| sale_id      | INTEGER  | Primary Key              |
| product_id   | INTEGER  | Foreign Key → Products(id) |
| quantity_sold| INTEGER  | > 0                      |
| timestamp    | DATETIME | Auto-generated           |

---

## Architecture Overview
```
User (CLI)
     ↓
StoreManager (Business Logic)
     ↓
Repositories (Data Access Layer)
     ↓
SQLite Database
```

- Models → Represent entities

- Repositories → Handle persistence

- StoreManager → Core business logic

- CLI → User interaction layer

---

## Core Concepts

- Encapsulation (protected stock control)

- Inheritance (PerishableProduct)

- Custom Exceptions (InsufficientStockError)

- Dictionary-based Search Optimization

- SQL Transaction Handling

- Memory-efficient data fetching

---

## Enhancements for better user experience

- Sale Preview + Confirmation before processing

- Dedicated Sale model for structured sales handling

- Reusable display functions

- Direct stock increase functionality

- Timezone-aware timestamp handling (Asia/Kolkata)

---

## Project Outcome

This project simulates a real-world retail backend system and demonstrates:

- Strong understanding of backend design

- Clean architectural layering and separation of concerns

- Efficient data handling using optimized in-memory structures

- Robust validation & error handling

- Practical business logic implementation

- Scalable and maintainable code structure

---


## Getting Started

### Prerequisites

- Python 3.10+

- SQLite

- pip

- Git (optional, for cloning)

---

### Installation

### 1️. Clone the Repository
```cmd
git clone https://github.com/CodeCaret/Smart-Stock-Retail-Management-System.git
cd Smart-Stock-Retail-Management-System
```

### 2. Create & Activate a Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 4. Run the Application
```cmd
python -m smart_stock_management
#or use batch file to run
```

---

## Application Workflow

1. User selects an option from CLI menu
2. StoreManager validates input
3. Business logic executes
4. Repository updates SQLite database
5. Result is displayed using reusable display functions
