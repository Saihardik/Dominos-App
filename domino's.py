

import sys
import time
import json
import os

# File to store users
USER_FILE = "users.json"

# Pizza Menu
PIZZA_MENU = {
    "Margherita": 150,
    "Farmhouse": 200,
    "Peppy Paneer": 220,
    "Veg Extravaganza": 250,
    "Chicken Dominator": 280
}

TOPPINGS = {
    "Extra Cheese": 30,
    "Mushrooms": 25,
    "Paneer": 40,
    "Chicken": 50,
}

# ---------------- User Management ----------------
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

def sign_up():
    users = load_users()
    print("\n🔐 Sign Up")
    username = input("Choose a username: ").strip()
    if username in users:
        print("❌ Username already exists. Try logging in.")
        return None
    password = input("Choose a password: ").strip()
    users[username] = {"password": password}
    save_users(users)
    print("✅ Sign up successful. Please log in.")
    return None

def log_in():
    users = load_users()
    print("\n🔓 Log In")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username in users and users[username]["password"] == password:
        print(f"✅ Welcome back, {username}!")
        return username
    print("❌ Invalid username or password.")
    return None

# ---------------- Pizza Classes ----------------
class Pizza:
    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price
        self.toppings = []

    def add_topping(self, topping):
        if topping in TOPPINGS:
            self.toppings.append(topping)

    def calculate_price(self):
        return self.base_price + sum(TOPPINGS[t] for t in self.toppings)

    def __str__(self):
        toppings_str = ", ".join(self.toppings) if self.toppings else "No toppings"
        return f"{self.name} ({toppings_str}) - ₹{self.calculate_price()}"

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, pizza):
        self.items.append(pizza)

    def view_cart(self):
        if not self.items:
            print("🛒 Cart is empty.")
            return
        print("\n🛒 Your Cart:")
        for i, pizza in enumerate(self.items, 1):
            print(f"{i}. {pizza}")
        print(f"Total: ₹{self.get_total()}")

    def get_total(self):
        return sum(p.calculate_price() for p in self.items)

    def checkout(self):
        if not self.items:
            print("🚫 Cart is empty. Cannot place order.")
            return
        print("\n✅ Placing order...")
        time.sleep(2)
        self.view_cart()
        print("🎉 Order placed successfully! Thank you for ordering from Domino's!")
        self.items.clear()

# ---------------- Menu & App Logic ----------------
def show_menu():
    print("\n🍕 Domino's Pizza Menu:")
    for name, price in PIZZA_MENU.items():
        print(f"- {name}: ₹{price}")

def show_toppings():
    print("\n🧀 Available Toppings:")
    for topping, price in TOPPINGS.items():
        print(f"- {topping}: ₹{price}")

def create_pizza():
    show_menu()
    choice = input("Enter pizza name: ")
    if choice not in PIZZA_MENU:
        print("❌ Invalid pizza selection.")
        return None
    pizza = Pizza(choice, PIZZA_MENU[choice])
    add_more = input("Add toppings? (y/n): ").lower()
    if add_more == 'y':
        show_toppings()
        while True:
            topping = input("Enter topping (or 'done' to finish): ")
            if topping.lower() == 'done':
                break
            if topping in TOPPINGS:
                pizza.add_topping(topping)
            else:
                print("❌ Invalid topping.")
    return pizza

def user_session(username):
    cart = Cart()
    while True:
        print(f"\n📱 Welcome, {username}")
        print("1. View Menu")
        print("2. Order Pizza")
        print("3. View Cart")
        print("4. Place Order")
        print("5. Logout")

        choice = input("Enter choice (1-5): ")
        if choice == '1':
            show_menu()
        elif choice == '2':
            pizza = create_pizza()
            if pizza:
                cart.add_item(pizza)
                print("✅ Pizza added to cart.")
        elif choice == '3':
            cart.view_cart()
        elif choice == '4':
            cart.checkout()
        elif choice == '5':
            print(f"👋 Logged out from {username}")
            break
        else:
            print("❌ Invalid choice. Try again.")

# ---------------- Main ----------------
def main():
    while True:
        print("\n===== Domino's CLI Login Menu =====")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Enter choice (1-3): ")
        if choice == '1':
            username = log_in()
            if username:
                user_session(username)
        elif choice == '2':
            sign_up()
        elif choice == '3':
            print("👋 Exiting... See you next time!")
            sys.exit()
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    main()
