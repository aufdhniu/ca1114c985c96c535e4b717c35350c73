from restaurant_pos_classes import (MenuItem, StaffRole, Staff, Table, Order, 
                      RestaurantReport, DataLoader)
from datetime import datetime, time

# Load data from CSV files
menu_items = DataLoader.load_menu_items('menu_items.csv')
staff_roles = DataLoader.load_staff_roles('staff_roles.csv')
tables = DataLoader.load_tables('tables.csv')

# Create report instance
restaurant_report = RestaurantReport()

# Create some staff members
server1 = Staff("S001", "John Smith", Staff.find_role(staff_roles, "Server"))
server2 = Staff("S002", "Jane Doe", Staff.find_role(staff_roles, "Server"))
manager = Staff("M001", "Mike Wilson", Staff.find_role(staff_roles, "Manager"))

# Simulate orders

# Order 1: Regular order
tables[0].set_status(TableStatus.OCCUPIED)
order1 = Order(tables[0], server1)
order1.add_item(next(item for item in menu_items if item.code == "APP01"), 2)  # 2 Spring Rolls
order1.add_item(next(item for item in menu_items if item.code == "ENT01"), 1)  # 1 Pad Thai
order1.add_item(next(item for item in menu_items if item.code == "DRK01"), 2)  # 2 Thai Iced Teas
order1.payment_method = "Credit Card"
order1.is_closed = True
restaurant_report.add_order(order1)

# Order 2: Order with void and comp
tables[2].set_status(TableStatus.OCCUPIED)
order2 = Order(tables[2], server2)
order2.add_item(next(item for item in menu_items if item.code == "ENT02"), 2)  # 2 Green Curry
order2.add_item(next(item for item in menu_items if item.code == "DRK02"), 2)  # 2 Sodas
order2.add_item(next(item for item in menu_items if item.code == "DES01"), 1)  # 1 Mango Sticky Rice
# Manager voids one item and comps another
order2.void_item(1, manager)  # Void the sodas
order2.comp_item(2, manager)  # Comp the dessert
order2.payment_method = "Cash"
order2.is_closed = True
restaurant_report.add_order(order2)

# Order 3: Large party
tables[5].set_status(TableStatus.OCCUPIED)
order3 = Order(tables[5], server1)
order3.add_item(next(item for item in menu_items if item.code == "APP02"), 3)  # 3 Chicken Wings
order3.add_item(next(item for item in menu_items if item.code == "ENT03"), 4)  # 4 Fried Rice
order3.add_item(next(item for item in menu_items if item.code == "DRK02"), 6)  # 6 Sodas
order3.add_item(next(item for item in menu_items if item.code == "DES01"), 2)  # 2 Mango Sticky Rice
order3.payment_method = "Credit Card"
order3.is_closed = True
restaurant_report.add_order(order3)

print("\n...GENERATING LUNCH SHIFT REPORT (11:00-15:00)...\n")

# Generate report for lunch hours only
restaurant_report.generate_report(
    start_time=time(11, 0),
    end_time=time(15, 0)
)