import requests
import json

# API endpoint
url = "http://ec2-13-127-61-77.ap-south-1.compute.amazonaws.com:8000/predict"

# Test data
test_data = {
    "age": 35,
    "income": 50000,
    "employment_length": 5,
    "loan_amount": 10000,
    "loan_term": 36,
    "credit_score": 700,
    "debt_to_income_ratio": 0.3,
    "education": "Bachelor",
    "marital_status": "Married",
    "housing": "Own",
    "purpose": "Home",
    "previous_loans": 1,
    "previous_defaults": 0
}

# Send POST request
try:
    response = requests.post(url, json=test_data)
    
    # Print response
    print("\nStatus Code:", response.status_code)
    print("\nResponse Headers:", response.headers)
    print("\nResponse Body:", json.dumps(response.json(), indent=2))
    
except Exception as e:
    print("Error:", str(e))

# Test multiple cases
test_cases = [
    {
        "name": "Good Credit",
        "data": {
            "age": 35,
            "income": 50000,
            "employment_length": 5,
            "loan_amount": 10000,
            "loan_term": 36,
            "credit_score": 700,
            "debt_to_income_ratio": 0.3,
            "education": "Bachelor",
            "marital_status": "Married",
            "housing": "Own",
            "purpose": "Home",
            "previous_loans": 1,
            "previous_defaults": 0
        }
    },
    {
        "name": "Risky Credit",
        "data": {
            "age": 25,
            "income": 30000,
            "employment_length": 1,
            "loan_amount": 20000,
            "loan_term": 60,
            "credit_score": 600,
            "debt_to_income_ratio": 0.5,
            "education": "High School",
            "marital_status": "Single",
            "housing": "Rent",
            "purpose": "Personal",
            "previous_loans": 2,
            "previous_defaults": 1
        }
    },
    {
        "name": "Excellent Credit",
        "data": {
            "age": 45,
            "income": 100000,
            "employment_length": 15,
            "loan_amount": 50000,
            "loan_term": 24,
            "credit_score": 800,
            "debt_to_income_ratio": 0.2,
            "education": "Master",
            "marital_status": "Married",
            "housing": "Own",
            "purpose": "Business",
            "previous_loans": 3,
            "previous_defaults": 0
        }
    }
]

print("\nTesting multiple cases:")
for case in test_cases:
    print(f"\nTest Case: {case['name']}")
    try:
        response = requests.post(url, json=case['data'])
        print("Status Code:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Error:", str(e)) 