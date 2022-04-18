import unittest
import json
from app import app

class ApiTest(unittest.TestCase):

    '''
    CHECKING FOR STATUS CODE 200
    test_getAllCustomers: checks if /customer endpoint is successful
    test_getAllOrders: checks if /order endpoint is successful
    test_deleteValidCustomer: checks if /customer/41 successfully deletes customer_id = 41
    '''

    def test_getAllCustomers(self):
        tester = app.test_client(self)
        response = tester.get("/customer")
        statusCode = response.status_code
        self.assertEqual(statusCode, 200)
    
    def test_getAllOrders(self):
        tester = app.test_client(self)
        response = tester.get("/order")
        statusCode = response.status_code
        self.assertEqual(statusCode, 200)

    
    def test_deleteValidCustomer(self):
        tester = app.test_client(self)
        response = tester.delete("/customer/41")
        statusCode = response.status_code
        self.assertEqual(statusCode, 200)
    
    '''
    CHECKING FOR STATUS 201
    test_validCustomerPost: Test for successful post method for endpoint /customer/create with valid json data
    '''
    
    def test_validCustomerPost(self):
        testData = {
            "dob" : "1989-12-01",
            "id" : 41,
            "name" : "test",
        }
        tester = app.test_client(self)
        response = tester.post("/customer/create", data = json.dumps(testData), content_type='application/json')
        statusCode = response.status_code
        self.assertEqual(statusCode, 201)

    '''
    CHECKING FOR STATUS 404
    test_invalidOrder: Test for endpoint /order?customer_id=300 for customer id that does not exist
    test_invalidEndpoint: Test for endpoint / that does not exist
   '''
    def test_invalidOrder(self):
        tester = app.test_client(self)
        response = tester.get("/order?customer_id=300")
        statusCode = response.status_code
        self.assertEqual(statusCode, 404)
    
    def test_invalidEndpoint(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statusCode = response.status_code
        self.assertEqual(statusCode, 404)

    '''
    CHECKING FOR STATUS 400
    test_invalidCustomerParameter: Test for endpoint /customer?number=x with invalid parameter x given
    test_invalidOrderParameter: Test for endpoint /order?customer_id=a with invalid parameter a given
    test_invalidCustomerPost: Test for unsuccessful post method for /customer/create using invalid data
    test_invalidCustomerDelete: Test for invalid deletion due to invalid customer id = 3000
    '''
    def test_invalidCustomerParameter(self):
        tester = app.test_client(self)
        response = tester.get("/customer?number=x")
        statusCode = response.status_code
        self.assertEqual(statusCode, 400)

    def test_invalidOrderParameter(self):
        tester = app.test_client(self)
        response = tester.get("/order?customer_id=a")
        statusCode = response.status_code
        self.assertEqual(statusCode, 400)

    def test_invalidCustomerPost(self):
        invalidTestData = {
            "do" : "1989-12-01",
            "id" : 41,
            "name" : "test",
        }
        tester = app.test_client(self)
        response = tester.post("/customer/create", data = json.dumps(invalidTestData), content_type='application/json')
        statusCode = response.status_code
        self.assertEqual(statusCode, 400)
    
    def test_invalidCustomerDelete(self):
        tester = app.test_client(self)
        response = tester.delete("/customer/3000")
        statusCode = response.status_code
        self.assertEqual(statusCode, 400)

    '''
    CHECK FOR STATUS 405
    test_invalidMethod: Checks for endpoint that exists but using wrong method - DEL /customer
    '''
    def test_invalidMethod(self):
        tester = app.test_client(self)
        response = tester.delete("/customer")
        statusCode = response.status_code
        self.assertEqual(statusCode, 405)
    
    '''
    CHECKING FOR CORRECT OUTPUT FORMAT (JSON)
    test_customerContent: Tests for json output for /customer endpoint
    test_orderContent: Tests for json output for /order endpoint
    '''
    def test_customerContent(self):
        tester = app.test_client(self)
        response = tester.get("/customer")
        self.assertEqual(response.content_type, "application/json")
    
    def test_orderContent(self):
        tester = app.test_client(self)
        response = tester.get("/order")
        self.assertEqual(response.content_type, "application/json")

    '''
    CHECKING FOR CORRECT DATA OUTPUT
    test_customerData: Tests if data output from /customer?number=3 endpoint is equal to expected output
    test_orderData: Tests if data output from /order?customer_id=1 endpoing is equal to expected output
    '''
    def test_customerData(self):
        expected_output = [
        {
            "dob": "1999-11-30",
            "id": 5,
            "name": "Ryan Sim"
        },
        {
            "dob": "1999-03-29",
            "id": 1,
            "name": "John Tan"
        },
        {
            "dob": "1998-11-05",
            "id": 4,
            "name": "Justin Kan"
        }
    ]
        tester = app.test_client(self)
        response = tester.get("/customer?number=3")
        self.assertEqual(list(json.loads(response.data)), expected_output)

    def test_orderData(self):
        expected_output = [
        {
            "customer_id": 1,
            "date_time": "2022-04-12T00:00:00",
            "item_name": "iPhone X",
            "item_price": 1300.0,
            "order_id": 1
        },
        {
            "customer_id": 1,
            "date_time": "2022-04-12T00:00:00",
            "item_name": "Apple",
            "item_price": 0.5,
            "order_id": 2
        }
    ]
        tester = app.test_client(self)
        response = tester.get("/order?customer_id=1")
        self.assertEqual(list(json.loads(response.data)), expected_output)

if __name__ == "__main__":
    unittest.main()
