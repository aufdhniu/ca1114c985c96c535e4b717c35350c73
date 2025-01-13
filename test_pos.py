import unittest
from restaurant_pos_classes import (MenuItem, StaffRole, Staff, Table, Order, 
                       TableStatus, RestaurantReport, OrderItem,
                       DataLoader)
from datetime import datetime, time

class TestRestaurantPOS(unittest.TestCase):
    def setUp(self):
        # Create test data
        self.menu_item = MenuItem("TEST1", "Test Item", 10.00, "Test")
        self.menu_item2 = MenuItem("TEST2", "Test Item 2", 15.00, "Test")
        
        self.staff_role = StaffRole("Server", 50, False, False)
        self.manager_role = StaffRole("Manager", 50, True, True)
        
        self.staff = Staff("S001", "Test Server", self.staff_role)
        self.manager = Staff("M001", "Test Manager", self.manager_role)
        
        self.table = Table(1, 4)
        
    def test_menu_item(self):
        """Test MenuItem class functionality"""
        self.assertEqual(self.menu_item.code, "TEST1")
        self.assertEqual(self.menu_item.name, "Test Item")
        self.assertEqual(self.menu_item.price, 10.00)
        self.assertEqual(self.menu_item.category, "Test")
        self.assertTrue(self.menu_item.available)
        
        # Test toggling availability
        self.menu_item.toggle_availability()
        self.assertFalse(self.menu_item.available)
        self.menu_item.toggle_availability()
        self.assertTrue(self.menu_item.available)
        
    def test_staff_role(self):
        """Test StaffRole class functionality"""
        self.assertEqual(self.staff_role.role, "Server")
        self.assertEqual(self.staff_role.discount, 50)
        self.assertFalse(self.staff_role.can_void)
        self.assertFalse(self.staff_role.can_comp)
        
        self.assertEqual(self.manager_role.role, "Manager")
        self.assertTrue(self.manager_role.can_void)
        self.assertTrue(self.manager_role.can_comp)
        
    def test_staff(self):
        """Test Staff class functionality"""
        self.assertEqual(self.staff.id, "S001")
        self.assertEqual(self.staff.name, "Test Server")
        self.assertEqual(self.staff.role, self.staff_role)
        self.assertEqual(len(self.staff.active_orders), 0)
        
        # Test role finding
        roles = [self.staff_role, self.manager_role]
        found_role = Staff.find_role(roles, "Manager")
        self.assertEqual(found_role, self.manager_role)
        
        # Test finding non-existent role
        not_found = Staff.find_role(roles, "Chef")
        self.assertIsNone(not_found)
        
    def test_table(self):
        """Test Table class functionality"""
        self.assertEqual(self.table.number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertEqual(self.table.status, TableStatus.AVAILABLE)
        self.assertIsNone(self.table.current_order)
        
        # Test status changes
        self.assertTrue(self.table.set_status(TableStatus.OCCUPIED))
        self.assertEqual(self.table.status, TableStatus.OCCUPIED)
        
        self.assertTrue(self.table.set_status(TableStatus.CLEANING))
        self.assertEqual(self.table.status, TableStatus.CLEANING)
        
        # Test invalid status
        self.assertFalse(self.table.set_status("Invalid"))
        self.assertEqual(self.table.status, TableStatus.CLEANING)
        
    def test_order_item(self):
        """Test OrderItem class functionality"""
        order_item = OrderItem(self.menu_item, 2)
        self.assertEqual(order_item.menu_item, self.menu_item)
        self.assertEqual(order_item.quantity, 2)
        self.assertFalse(order_item.voided)
        self.assertFalse(order_item.comped)
        
        # Test total calculation
        self.assertEqual(order_item.get_total(), 20.00)
        
        # Test voided item
        order_item.voided = True
        self.assertEqual(order_item.get_total(), 0.00)
        
        # Test comped item
        order_item.voided = False
        order_item.comped = True
        self.assertEqual(order_item.get_total(), 0.00)
        
    def test_order(self):
        """Test Order class functionality"""
        order = Order(self.table, self.staff)
        
        # Test initial state
        self.assertEqual(order.table, self.table)
        self.assertEqual(order.staff, self.staff)
        self.assertEqual(len(order.items), 0)
        self.assertFalse(order.is_closed)
        self.assertIsNone(order.payment_method)
        
        # Test adding items
        self.assertTrue(order.add_item(self.menu_item, 2))
        self.assertEqual(len(order.items), 1)
        
        # Test adding unavailable item
        self.menu_item2.toggle_availability()  # Make unavailable
        self.assertFalse(order.add_item(self.menu_item2, 1))
        
        # Test totals
        self.assertEqual(order.get_subtotal(), 20.00)
        self.assertAlmostEqual(order.get_total(), 21.40, places=2)  # with 7% tax
        self.assertEqual(order.get_total(include_tax=False), 20.00)
        
        # Test void permissions
        self.assertFalse(order.void_item(0, self.staff))  # Server can't void
        self.assertTrue(order.void_item(0, self.manager))  # Manager can void
        
        # Test comp permissions
        order.add_item(self.menu_item, 1)
        self.assertFalse(order.comp_item(1, self.staff))  # Server can't comp
        self.assertTrue(order.comp_item(1, self.manager))  # Manager can comp
        
        # Test closed order
        order.is_closed = True
        self.assertFalse(order.add_item(self.menu_item, 1))
        
    def test_restaurant_report(self):
        """Test RestaurantReport class functionality"""
        report = RestaurantReport()
        
        # Create some orders
        order1 = Order(self.table, self.staff)
        order1.add_item(self.menu_item, 2)
        order1.payment_method = "Cash"
        order1.is_closed = True
        
        order2 = Order(self.table, self.manager)
        order2.add_item(self.menu_item, 1)
        order2.payment_method = "Credit Card"
        order2.is_closed = True
        
        # Add orders to report
        report.add_order(order1)
        report.add_order(order2)
        
        # Test report generation (basic check that it doesn't raise errors)
        report.generate_report()
        report.generate_report(
            start_time=time(9, 0),
            end_time=time(17, 0)
        )
        
    def test_data_loader(self):
        """Test DataLoader class functionality"""
        # Test loading menu items
        menu_items = DataLoader.load_menu_items('menu_items.csv')
        self.assertGreater(len(menu_items), 0)
        self.assertIsInstance(menu_items[0], MenuItem)
        
        # Test loading staff roles
        staff_roles = DataLoader.load_staff_roles('staff_roles.csv')
        self.assertGreater(len(staff_roles), 0)
        self.assertIsInstance(staff_roles[0], StaffRole)
        
        # Test loading tables
        tables = DataLoader.load_tables('tables.csv')
        self.assertGreater(len(tables), 0)
        self.assertIsInstance(tables[0], Table)

if __name__ == '__main__':
    unittest.main()