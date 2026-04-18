import json
import os
from datetime import datetime

# --- 1. Product Class ---
class Product:
    def __init__(self, id, name, price, stock):
        self.id = str(id)
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "stock": self.stock}

    @staticmethod
    def from_dict(data):
        return Product(data['id'], data['name'], data['price'], data['stock'])

# --- 2. Invoice Item Class ---
class InvoiceItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

# --- 3. Invoice Class ---
class Invoice:
    TAX_RATE = 0.05

    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = []
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_item(self, product, quantity):
        item = InvoiceItem(product, quantity)
        self.items.append(item)
        self.calculate_total()

    def remove_item(self, product_id):
        for item in self.items:
            if item.product.pid == str(product_id):
                item.product.stock += item.quantity 
                self.items.remove(item)
                self.calculate_total()
                return True, item.product.name
        return False, None

    def calculate_total(self):
        self.subtotal = sum(item.total_price for item in self.items)
        self.tax = self.subtotal * self.TAX_RATE
        self.total = self.subtotal + self.tax

    def generate_bill_string(self):
        bill =  f"\n{'='*45}\n"
        bill += f"{'INVOICEPRO BILLING SYSTEM':^45}\n"
        bill += f"{'='*45}\n"
        bill += f"Customer: {self.customer_name}\n"
        bill += f"Date:     {self.date}\n"
        bill += f"{'-'*45}\n"
        bill += f"{'Item':<20} {'Qty':<5} {'Price':<8} {'Total':<7}\n"
        for item in self.items:
            bill += f"{item.product.name:<20} {item.quantity:<5} {item.product.price:<8.2f} {item.total_price:<7.2f}\n"
        bill += f"{'-'*45}\n"
        bill += f"{'Subtotal:':<32} ${self.subtotal:>10.2f}\n"
        bill += f"{'Tax (5%):':<32} ${self.tax:>10.2f}\n"
        bill += f"{'GRAND TOTAL:':<32} ${self.total:>10.2f}\n"
        bill += f"{'='*45}\n"
        bill += f"{'Visit Again!':^45}\n"
        bill += f"{'='*45}\n"
        return bill

# --- 4. Inventory Manager Class ---
class InventoryManager:
    def __init__(self, filename="products.json"):
        # This part ensures the JSON file stays in the same folder as invoice_pro.py
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(self.base_dir, filename)
        self.products = self.load_products()

    def load_products(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return {str(p['id']): Product.from_dict(p) for p in data}
            except: return {}
        return {}

    def save_products(self):
        with open(self.filename, 'w') as f:
            json.dump([p.to_dict() for p in self.products.values()], f, indent=4)

    def add_product(self,id, name, price, stock):
        self.products[str(id)] = Product(id, name, price, stock)
        self.save_products()

    def delete_product(self, id):
        id = str(id)
        if id in self.products:
            name = self.products[id].name
            del self.products[id]
            self.save_products()
            return True, name
        return False, None

# --- Main Logic ---

def main():
    manager = InventoryManager()
    
    while True:
        print("\n--- INVOICEPRO MAIN MENU ---")
        print("1. Manage Inventory (Add/View/Delete)")
        print("2. Create New Invoice")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            while True:
                print("\n--- INVENTORY MANAGEMENT ---")
                print("a. Add Product")
                print("b. View All Products")
                print("c. Delete Product (from Database)")
                print("d. Back to Main Menu")
                sub_choice = input("Select (a/b/c/d): ").lower()

                if sub_choice == 'a':
                    pid = input("ID: "); name = input("Name: ")
                    try:
                        price = float(input("Price: ")); stock = int(input("Stock: "))
                        manager.add_product(id, name, price, stock)
                        print(f"Product '{name}' saved.")
                    except ValueError:
                        print("Error: Invalid price or stock format.")
                elif sub_choice == 'b':
                    print(f"\n{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<10}")
                    for p in manager.products.values():
                        print(f"{p.id:<10} {p.name:<20} ${p.price:<9.2f} {p.stock:<10}")
                elif sub_choice == 'c':
                    id = input("Enter ID to delete: ")
                    success, name = manager.delete_product(id)
                    print(f"Deleted {name}" if success else "Not found.")
                elif sub_choice == 'd': break

        elif choice == '2':
            cust = input("Customer Name: ")
            inv = Invoice(cust)
            while True:
                print("\nCommands: [ID] to add, 'del' to remove entry, 'done' to finish")
                id = input("Entry: ").lower()
                if id == 'done': break
                elif id == 'del':
                    rid = input("ID to remove from bill: ")
                    success, name = inv.remove_item(rid)
                    print(f"Removed {name}" if success else "Not in bill.")
                elif id in manager.products:
                    try:
                        qty = int(input(f"Quantity for {manager.products[id].name}: "))
                        if manager.products[id].update_stock(qty):
                            inv.add_item(manager.products[id], qty)
                        else: print("Out of stock!")
                    except ValueError:
                        print("Error: Please enter a number for quantity.")
                else: print("Invalid ID.")

            if inv.items:
                bill = inv.generate_bill_string()
                print(bill)
                
                # Save physical receipt file in the same folder as the script
                filename = f"Invoice_{cust.replace(' ', '_')}.txt"
                file_path = os.path.join(manager.base_dir, filename)
                
                with open(file_path, "w") as f:
                    f.write(bill)
                
                manager.save_products()
                print(f"Invoice Finalized and saved as: {filename}")
            else:
                print("No items added. Invoice cancelled.")

        elif choice == '3':
            print("Closing InvoicePro. Goodbye!")
            break

if __name__ == "__main__":
    main()