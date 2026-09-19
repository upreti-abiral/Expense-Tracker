# Expense Tracker

A desktop expense tracking application built with Python, Tkinter, SQLite, and Matplotlib.

## Overview

This project is a desktop application for recording and managing daily expenses.

Expenses are stored in a local SQLite database and can be viewed in a table. The application also provides charts showing spending by category and daily spending over the last 30 days.

The project was built to practise GUI development, database management, data validation, and data visualisation in Python.

## Features

- Add expenses
- View saved expenses
- Delete selected expenses
- Choose expense categories
- Record expense dates
- Add descriptions
- Store data locally using SQLite
- View spending by category
- View daily spending
- Display charts using Matplotlib
- Validate amounts and dates

## Categories

The available categories are:

- Food
- Transport
- Shopping
- Bills
- Study
- Other

## Charts

The application includes two charts:

### Spending by Category

A pie chart showing how expenses are distributed across categories.

### Daily Spending

A bar chart showing total spending for each day.

Both charts use expense data from the last 30 days.

## How It Works

When an expense is added, the application stores its:

- Amount
- Category
- Date
- Description

in a local SQLite database.

The application then displays the saved expenses in a table.

Users can also select one or more expenses and delete them.

The Charts section retrieves data from the database and uses Matplotlib to display spending information visually.

## Project Structure

Expense-Tracker/
├── app.py
├── db.py
├── requirements.txt
├── expenses.db
└── README.md

## Files

`app.py`  
Handles the graphical interface, user input, expense management, and charts.

`db.py`  
Handles SQLite database creation, storing expenses, retrieving data, deleting expenses, and calculating totals.

`expenses.db`  
Local SQLite database created automatically when the application runs.

`requirements.txt`  
Contains the external Python dependency required by the project.

`README.md`  
Project documentation.

## Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib

## Requirements

- Python 3.8 or newer
- Tkinter
- SQLite3
- Matplotlib

Install the required library with:

    pip install -r requirements.txt

## How to Run

Install the dependency:

    pip install -r requirements.txt

Run the application:

    python app.py

The `expenses.db` database will be created automatically if it does not already exist.

## Database

The application uses an `expenses` table with the following fields:

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Unique expense ID |
| `amount` | REAL | Expense amount |
| `category` | TEXT | Expense category |
| `date` | TEXT | Date of the expense |
| `description` | TEXT | Optional description |

## Data Validation

The application checks that:

- The amount is a valid number
- The amount is greater than zero
- The date follows the `YYYY-MM-DD` format

## Concepts Practised

- Tkinter GUI development
- SQLite databases
- CRUD operations
- Classes and methods
- Input validation
- Exception handling
- Working with dates
- SQL queries
- Data aggregation
- Data visualisation
- Integrating Matplotlib with Tkinter

## Possible Improvements

- Edit existing expenses
- Add monthly summaries
- Add expense budgets
- Add more chart types
- Search and filter expenses
- Export expenses to CSV
- Add recurring expenses

These features are not currently implemented.

## Author

Abiral Upreti

A Python project focused on practising application development, database management, and data visualisation.
