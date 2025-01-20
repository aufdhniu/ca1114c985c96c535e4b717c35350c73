from typing import List, Dict, Optional
from datetime import datetime, time
import csv

class MenuItem:
    def __init__(self, code: str, name: str, price: float, category: str):
        self.code = code
        self.name = name
        self.price = price
        self.category = category
        self.available = True

    def toggle_availability(self):
        self.available = not self.available


class StaffRole:
    def __init__(self, role: str, discount: int, can_void: bool, can_comp: bool):
        self.role = role
        self.discount = discount
        self.can_void = can_void
        self.can_comp = can_comp


class Staff:
    def __init__(self, id: str, name: str, role: StaffRole):
        self.id = id
        self.name = name
        self.role = role
        self.active_orders: list[Order] = []

    @staticmethod
    def find_role(roles: list[StaffRole], position: str) -> Optional[StaffRole]:
        for role in roles:
            if role.role == position:
                return role
        return None


class TableStatus:
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    RESERVED = "Reserved"
    CLEANING = "Cleaning"


class Table:
    def __init__(self, number: int, capacity: int):
        self.number = number
        self.capacity = capacity
        self.status = TableStatus.AVAILABLE
        self.current_order: Optional[Order] = None

    def set_status(self, status: str) -> bool:
        if status in [TableStatus.AVAILABLE, TableStatus.OCCUPIED, TableStatus.RESERVED, TableStatus.CLEANING]:
            self.status = status
            return True
        return False


class OrderItem:
    def __init__(self, menu_item: MenuItem, quantity: int):
        self.menu_item = menu_item
        self.quantity = quantity
        self.voided = False
        self.comped = False

    def get_total(self) -> float:
        if self.voided or self.comped:
            return 0.0
        return self.menu_item.price * self.quantity


class Order:
    TAX_RATE = 0.07

    def __init__(self, table: Table, staff: Staff):
        self.table = table
        self.staff = staff
        self.items: List[OrderItem] = []
        self.is_closed = False
        self.payment_method: Optional[str] = None

    def add_item(self, menu_item: MenuItem, quantity: int) -> bool:
        if self.is_closed or not menu_item.available:
            return False
        self.items.append(OrderItem(menu_item, quantity))
        return True

    def void_item(self, index: int, staff: Staff) -> bool:
        if index < 0 or index >= len(self.items):
            return False
        if not staff.role.can_void:
            return False
        self.items[index].voided = True
        return True

    def comp_item(self, index: int, staff: Staff) -> bool:
        if index < 0 or index >= len(self.items):
            return False
        if not staff.role.can_comp:
            return False
        self.items[index].comped = True
        return True

    def get_subtotal(self) -> float:
        return sum(item.get_total() for item in self.items)

    def get_total(self, include_tax: bool = True) -> float:
        subtotal = self.get_subtotal()
        if include_tax:
            return subtotal * (1 + self.TAX_RATE)
        return subtotal


class RestaurantReport:
    def __init__(self):
        self.orders: List[Order] = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def generate_report(self, start_time: Optional[time] = None, end_time: Optional[time] = None):
        total_sales = 0
        print("\n--- Restaurant Report ---")
        for order in self.orders:
            print(f"Table: {order.table.number}, Total: {order.get_total():.2f}")
            total_sales += order.get_total()
        print(f"Total Sales: {total_sales:.2f}\n")


class DataLoader:
    @staticmethod
    def load_menu_items(file_path: str) -> list[MenuItem]:
        menu_items = []
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for line in csv_reader:
                menu_items.append(MenuItem(line['Code'], line['Name'], float(line['Price']), line['Category']))
        return menu_items

    @staticmethod
    def load_staff_roles(file_path: str) -> list[StaffRole]:
        staff_roles = []
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for line in csv_reader:
                staff_roles.append(StaffRole(line['Role'], int(line['Discount']), line['CanVoid'] == 'True', line['CanComp'] == 'True'))
        return staff_roles

    @staticmethod
    def load_tables(file_path: str) -> list[Table]:
        tables = []
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for line in csv_reader:
                tables.append(Table(int(line['Number']), int(line['Capacity'])))
        return tables