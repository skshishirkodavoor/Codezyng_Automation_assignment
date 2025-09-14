"""
Data utilities for handling Excel, CSV, and JSON data
"""
import pandas as pd
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger


class DataUtils:
    """Utility class for handling test data from various sources"""
    
    def __init__(self, data_dir="tests/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def read_excel_data(self, file_path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """Read data from Excel file"""
        try:
            file_path = self.data_dir / file_path
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            # Convert DataFrame to list of dictionaries
            data = df.to_dict('records')
            logger.info(f"Successfully read {len(data)} records from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to read Excel data from {file_path}: {str(e)}")
            raise
    
    def read_csv_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Read data from CSV file"""
        try:
            file_path = self.data_dir / file_path
            df = pd.read_csv(file_path)
            data = df.to_dict('records')
            logger.info(f"Successfully read {len(data)} records from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to read CSV data from {file_path}: {str(e)}")
            raise
    
    def read_json_data(self, file_path: str) -> Dict[str, Any]:
        """Read data from JSON file"""
        try:
            file_path = self.data_dir / file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"Successfully read JSON data from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to read JSON data from {file_path}: {str(e)}")
            raise
    
    def write_excel_data(self, data: List[Dict[str, Any]], file_path: str, sheet_name: str = "Sheet1"):
        """Write data to Excel file"""
        try:
            file_path = self.data_dir / file_path
            df = pd.DataFrame(data)
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
            logger.info(f"Successfully wrote {len(data)} records to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to write Excel data to {file_path}: {str(e)}")
            raise
    
    def write_csv_data(self, data: List[Dict[str, Any]], file_path: str):
        """Write data to CSV file"""
        try:
            file_path = self.data_dir / file_path
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            logger.info(f"Successfully wrote {len(data)} records to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to write CSV data to {file_path}: {str(e)}")
            raise
    
    def write_json_data(self, data: Dict[str, Any], file_path: str):
        """Write data to JSON file"""
        try:
            file_path = self.data_dir / file_path
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            logger.info(f"Successfully wrote JSON data to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to write JSON data to {file_path}: {str(e)}")
            raise
    
    def get_test_data_for_login(self) -> List[Dict[str, str]]:
        """Get test data for login scenarios"""
        return [
            {"username": "demo@opencart.com", "password": "demo", "expected": "success"},
            {"username": "invalid@test.com", "password": "wrong", "expected": "failure"},
            {"username": "", "password": "demo", "expected": "failure"},
            {"username": "demo@opencart.com", "password": "", "expected": "failure"},
        ]
    
    def get_test_data_for_registration(self) -> List[Dict[str, str]]:
        """Get test data for registration scenarios"""
        return [
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
            }
        ]
    
    def get_test_data_for_checkout(self) -> List[Dict[str, str]]:
        """Get test data for checkout scenarios"""
        return [
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
                "expected": "success"
            }
        ]
    
    def filter_data_by_condition(self, data: List[Dict[str, Any]], condition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter data based on condition"""
        try:
            filtered_data = []
            for record in data:
                match = True
                for key, value in condition.items():
                    if record.get(key) != value:
                        match = False
                        break
                if match:
                    filtered_data.append(record)
            
            logger.info(f"Filtered {len(filtered_data)} records from {len(data)} total records")
            return filtered_data
            
        except Exception as e:
            logger.error(f"Failed to filter data: {str(e)}")
            raise
    
    def get_random_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get random record from data"""
        try:
            import random
            random_record = random.choice(data)
            logger.debug(f"Selected random record: {random_record}")
            return random_record
            
        except Exception as e:
            logger.error(f"Failed to get random data: {str(e)}")
            raise
