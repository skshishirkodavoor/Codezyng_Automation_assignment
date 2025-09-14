
from utils.data_utils import DataUtils


def create_sample_test_data():
    """Create sample test data files"""
    data_utils = DataUtils()
    
    # Login test data
    login_data = [
        {"username": "demo@opencart.com", "password": "demo", "expected": "success"},
        {"username": "shishr@test.com", "password": "wrong", "expected": "failure"},
        {"username": "", "password": "demo", "expected": "failure"},
        {"username": "demo@opencart.com", "password": "", "expected": "failure"},
        {"username": "test@codezyng.com", "password": "codezyng", "expected": "failure"},
    ]
    
    # Registration test data
    registration_data = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@test.com",
            "telephone": "1234567890",
            "password": "password123",
            "confirm_password": "password123",
            "expected": "success"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@test.com",
            "telephone": "0987654321",
            "password": "password456",
            "confirm_password": "password456",
            "expected": "success"
        },
        {
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob.johnson@test.com",
            "telephone": "5555555555",
            "password": "password789",
            "confirm_password": "different_password",
            "expected": "failure"
        }
    ]
    
    # Checkout test data
    checkout_data = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "company": "Test Company",
            "address_1": "123 Test Street",
            "address_2": "Apt 1",
            "city": "Test City",
            "postcode": "12345",
            "country": "United States",
            "region": "California",
            "email": "john.doe@test.com",
            "telephone": "1234567890",
            "expected": "success"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "company": "Another Company",
            "address_1": "456 Another Street",
            "address_2": "Suite 2",
            "city": "Another City",
            "postcode": "54321",
            "country": "United States",
            "region": "New York",
            "email": "jane.smith@test.com",
            "telephone": "0987654321",
            "expected": "success"
        }
    ]
    
    # Product search data
    search_data = [
        {"search_term": "iPhone", "expected_results": True},
        {"search_term": "Samsung", "expected_results": True},
        {"search_term": "MacBook", "expected_results": True},
        {"search_term": "Canon", "expected_results": True},
        {"search_term": "Nikon", "expected_results": True},
        {"search_term": "xyz123nonexistent", "expected_results": False},
    ]
    
    # Coupon codes
    coupon_data = [
        {"code": "WELCOME10", "discount": 10, "type": "percentage"},
        {"code": "SAVE20", "discount": 20, "type": "percentage"},
        {"code": "FREESHIP", "discount": 0, "type": "shipping"},
        {"code": "INVALID123", "discount": 0, "type": "invalid"},
    ]
    
    # Create Excel files
    try:
        data_utils.write_excel_data(login_data, "login_test_data.xlsx", "Login")
        data_utils.write_excel_data(registration_data, "registration_test_data.xlsx", "Registration")
        data_utils.write_excel_data(checkout_data, "checkout_test_data.xlsx", "Checkout")
        data_utils.write_excel_data(search_data, "search_test_data.xlsx", "Search")
        data_utils.write_excel_data(coupon_data, "coupon_test_data.xlsx", "Coupons")
        
        print("Sample test data files created successfully!")
        
    except Exception as e:
        print(f"Failed to create test data files: {str(e)}")


if __name__ == "__main__":
    create_sample_test_data()
