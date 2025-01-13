# ca1114c985c96c535e4b717c35350c73


# Restaurant POS System Assignment

## Overview
In this assignment, you will practice reverse engineering by analyzing provided code and implementing a Restaurant Point of Sale (POS) System. You'll need to study the test cases and example usage to determine what methods and attributes each class should have.

## Files Provided
- `my_classes.py` - Contains empty class definitions that you need to implement
- `menu_items.csv` - Restaurant menu data
- `staff_roles.csv` - Staff role definitions and permissions
- `tables.csv` - Restaurant table information
- `homework.py` - Example usage of the system
- `test_pos.py` - Unit tests that your implementation must pass

## Your Task

### Step 1: Analyze the Code
1. Study `homework.py` to understand:
   - How the classes are used
   - What operations are performed
   - Required attributes and methods

2. Study `test_pos.py` to understand:
   - Expected behavior of each class
   - Required method signatures
   - Edge cases that need to be handled

### Step 2: Class Implementation
Implement the following empty classes in `my_classes.py`:
```python
class MenuItem:
    pass

class StaffRole:
    pass
        
class Staff:
    pass

class Table:
    pass

class OrderItem:
    pass

class Order:
    pass

class RestaurantReport:
    pass

class DataLoader:
    pass
```

Your implementation should:
- Use appropriate type hints
- Handle all test cases
- Support all operations shown in homework.py

### Step 3: Testing
Verify your implementation by:
1. Running the unit tests:
```bash
python -m unittest test_pos.py
```
2. Running the example program:
```bash
python homework.py
```

## Hints for Reverse Engineering
1. **Start with Data Analysis**
   - Look at the CSV files to understand the data structure
   - Note what fields are available in each file

2. **Method Discovery**
   - Look for method calls in homework.py
   - Check test assertions to find required methods
   - Pay attention to return types from the test cases

3. **Attribute Discovery**
   - Look for attribute access in the code
   - Check object initialization in the tests
   - Note what data needs to be stored

4. **Type Hints**
   - Study any error messages related to types
   - Look at parameter and return value usage

5. **Business Logic**
   - Notice patterns in how objects interact
   - Look for validation and permission checks
   - Study how calculations are performed

## Submission Requirements
1. Submit your completed `my_classes.py` file
2. Do not modify any other files
3. All tests must pass
4. The example program must run without errors

## Important Notes
- Use Python 3.7 or higher
- Don't modify class names or add new classes
- Focus on understanding the existing code structure
- Think about why each method and attribute is needed

## Getting Started
1. Read through homework.py and test_pos.py carefully
2. Make notes of methods being called and attributes being accessed
3. Create a checklist of features to implement
4. Implement one class at a time, testing as you go