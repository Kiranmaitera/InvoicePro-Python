# InvoicePro-Python
A terminal based  billing and inventory management system built with python and OOP.
# InvoicePro – Console Invoice Generator

A robust terminal-based billing system for small stores that manages products, tracks inventory, and generates professional text-based invoices.

## 🚀 Key Features
- **Inventory Management:** Add, view, and delete products from a persistent database.
- **Dynamic Invoicing:** Real-time subtotal, tax (5%), and grand total calculations.
- **Session Editing:** Remove wrong entries from a bill before finalizing.
- **Persistence:** Uses JSON for inventory and generates .txt receipts for every sale.

## 🛠️ Technical Stack
- **Language:** Python 3.x
- **Concepts:** Object-Oriented Programming (OOP), File I/O, Data Serialization (JSON).
- **Libraries:** `os`, `json`, `datetime`.

## 📂 Project Structure
- `invoice_pro.py`: Core application logic.
- `products.json`: Auto-generated database file.
- `Invoice_CustomerName.txt`: Sample output generated after checkout.

## 📖 How to Run
1. Clone the repository.
2. Run `python invoice_pro.py`.
3. Follow the terminal prompts to manage inventory or create bills.
