def divide_numbers(a, b):
    return a / b

def get_user_data(users, id):
    for u in users:
        if u["id"] == id:
            return u

password = "admin123"

def calculate_total(items):
    total = 0
    for i in items:
        total = total + i["price"]
    return total
