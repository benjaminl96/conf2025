# Developing log file for customer purchase and order fulfillment actions
fields = [
    "timestamp",
    "customer_id",
    "order_id",
    "product_id",
    "quantity",
    "status"
]

customers = {}
statuses = ["placed", "processed", "shipped", "delivered", "returned", "refunded"]
products = ["selfie stick", "smart watch", "wireless earbuds", "fitness tracker", "VR headset"]

import random
import time
import string
from faker import Faker
import os
import json

fake = Faker()

CUSTOMERS_FILE = "customers.json"
if os.path.exists(CUSTOMERS_FILE):
    with open(CUSTOMERS_FILE, "r") as f:
        customers = json.load(f)
else:
    customers = {}

def random_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# Weighted choices for number of products per order
product_count_weights = [1]*70 + [2]*20 + [3]*7 + [4]*2 + [5]*1

for _ in range(100):
    log = {}
    log["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 10% chance of a new customer
    if random.random() < 0.1 or len(customers) == 0:
        customer_id = fake.email()
        order_id = random_id(10)
        num_products = random.choice(product_count_weights)
        product_id = random.sample(products, num_products)
        quantity = random.randint(1, 5)
        status = "placed"
        customers[customer_id] = {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "status": status
        }
    else:
        customer_id = random.choice(list(customers.keys()))
        order_info = customers[customer_id]
        order_id = order_info["order_id"]
        product_id = order_info["product_id"]
        quantity = order_info["quantity"]
        current_status_index = statuses.index(order_info["status"])
        # If status is 'refunded' or 'delivered', start a new order
        if order_info["status"] in ["refunded", "delivered"]:
            order_id = random_id(10)
            num_products = random.choice(product_count_weights)
            product_id = random.sample(products, num_products)
            quantity = random.randint(1, 5)
            status = "placed"
            customers[customer_id] = {
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "status": status
            }
        # If status is 'returned', always follow with 'refunded'
        elif order_info["status"] == "returned":
            status = "refunded"
            customers[customer_id]["status"] = status
        # If status is not the last, increment status
        elif current_status_index < len(statuses) - 2:
            # Make 'returned' rare (e.g., 5% chance), otherwise normal progression
            if statuses[current_status_index + 1] == "returned" and random.random() < 0.05:
                status = "returned"
                customers[customer_id]["status"] = status
            else:
                status = statuses[current_status_index + 1]
                customers[customer_id]["status"] = status
        else:
            status = order_info["status"]

    log["customer_id"] = customer_id
    log["order_id"] = order_id
    log["product_id"] = product_id
    log["quantity"] = quantity
    log["status"] = status

    # Print product_id as a semicolon-separated string for CSV output
    log_out = log.copy()
    log_out["product_id"] = ";".join(log["product_id"]) if isinstance(log["product_id"], list) else log["product_id"]
    print(",".join(str(log_out[field]) for field in fields))
    time.sleep(0.01)  # Simulate time delay between logs

# Save customers to file at the end
with open(CUSTOMERS_FILE, "w") as f:
    json.dump(customers, f)




