import unittest
import json
import requests
from msal import ConfidentialClientApplication
from jsuser import get_user_principal_names

class TestYourModule(unittest.TestCase):
    def setUp(self):
        # Set up the test data and environment
        self.client_id = "45ad3485-3466-429a-9b2d-dde3b53656fe"
        self.client_secret = "FPz8Q~dOqMyILUejgocJRq2Cd-ljSJan-sMw.dq8"
        self.tenant_id = "5fe5e79b-0daf-404f-9bde-0a3bff7b1328"
        self.access_token = "YOUR_ACCESS_TOKEN"

    def test_get_user_principal_names(self):
        # Prepare the expected user principal names
        expected_user_principal_names = ["user1@example.com", "user2@example.com"]

        # Mock the response from the requests library
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        # Mock the requests library's get() method
        def mock_get(url, headers):
            response_data = {
                "value": [
                    {"userPrincipalName": "user1@example.com"},
                    {"userPrincipalName": "user2@example.com"}
                ]
            }
            return MockResponse(response_data, 200)

        # Patch the requests.get() method with our mock_get() method
        requests.get = mock_get

        # Call the function to be tested
        result = get_user_principal_names(self.access_token)

        # Assert the result
        self.assertEqual(result, expected_user_principal_names)

if __name__ == '__main__':
    unittest.main()
