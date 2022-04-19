# Kinexcs Backend Assessment

## Technology

Flask, Marshmallow, SQLAlchemy, POSTGRESQL

## API Endpoints

### **Get Customers**

Returns json data about all the customers.

- **URL**</br>
  /customer
- **Method:**</br>
  `GET`
- **URL Parameters:**</br>
  None
- **Success Response:**

  - **Code:** 200 </br>
    **Content:** </br>
    `{{"id": 1, "name": "John Tan", "dob": "1999-03-29"}, {"id": 2, "name": "Jane Doe", "dob": "1987-11-05"}, ...}`

- **Error Response:**
  None
- **Sample Call:**

```
import requests
response = requests.get('/customer')
print(response)
```

### **Get Orders**

Returns json data about all orders.

- **URL**</br>
  /order
- **Method:**</br>
  `GET`
- **URL Parameters:**</br>
  None
- **Success Response:**

  - **Code:** 200 </br>
    **Content:** </br>
    `{{"customer_id": 1, "date_time": "2022-04-12T00:00:00", "item_name": "iPhone X", "item_price": 1300.0, "order_id": 1}, ...`

- **Error Response:**
  None
- **Sample Call:**

```
import requests
response = requests.get('/order')
print(response)
```

### **Get All Orders From Customer**

Returns json data about all orders made by a single customer.

- **URL**</br>
  /order?customer_id=x
- **Method:**</br>
  `GET`
- **URL Parameters:**</br>
  **Required:** </br>
  `x = [integer]`
- **Success Response:**

  - **Code:** 200 </br>
    **Content:** </br>
    `{{"customer_id": 1, "date_time": "2022-04-12T00:00:00", "item_name": "iPhone X", "item_price": 1300.0, "order_id": 1}, {"customer_id": 1, "date_time": "2022-04-12T00:00:00", "item_name": "Apple", "item_price": 0.5, "order_id": 2}}`

- **Error Response:**

  - **Code:** 404 </br>
    **Content:** </br>
    `{"error" : 404, "message" : "customer_id 3 not found"}`

    OR

  - **Code:** 400 </br>
    **Content:** </br>
    `{"error": 400, "message": "Bad Request: URL Parameter customer_id = a is not valid. URL parameter must be an integer."}`

- **Sample Call:**

```
import requests
response = requests.get('/order?customer_id=1')
print(response)
```

### **Get Youngest Customers**

Returns json data about youngest customers in the database.

- **URL**</br>
  /customer?number=n
- **Method:**</br>
  `GET`
- **URL Parameters:**</br>
  **Required:** </br>
  `n = [integer]`
- **Success Response:**

  - **Code:** 200 </br>
    **Content:** </br>
    `{{"dob": "1999-11-30", "id": 5, "name": "Ryan Sim"}, {"dob": "1999-03-29", "id": 1, "name": "John Tan"}`

- **Error Response:**

  - **Code:** 400 </br>
    **Content:** </br>
    `{"error": 400, "message": "Bad Request: URL Parameter number = a is not valid. URL parameter must be an integer."}`

- **Sample Call:**

```
import requests
response = requests.get('/customer?number=2')
print(response)
```

### **Create Customer**

Creates a customer in the database.

- **URL**</br>
  /customer/create
- **Method:**</br>
  `POST`
- **URL Parameters:**</br>
  None
- **Data Parameters:**<br>

  - **Required:**<br>

    ```
    JSON DATA
    {
        "id": [integer]
        "name": [string]
        "dob": [Date (YYYY-MM-DD)]
    }
    ```

- **Success Response:**

  - **Code:** 201 </br>
    **Content:** </br>
    `{"code": 201, "message": Data added successfully"}`

- **Error Response:**

  - **Code:** 400 </br>
    **Content:** </br>
    `{"error": 400, "message": "Bad Request: Validation for inputs failed. Please check the format of the data inputted."}`

    OR

  - **Code:** 400 </br>
    **Content:** </br>
    `{"error": 400, "message": "customer_id 1 already exists, please use another id"}`

    OR

  - **Code:** 400 </br>
    **Content:** </br>
    `{"error": 400, "message": "Bad Request: Failed to decode JSON input. Please check the formatting of the JSON input."}`

- **Sample Call:**

```
import requests

data = {
    "id" = 2,
    "name" = "Bob",
    "dob" = "2019-12-31"
}
response = requests.post('/customer/create', data = json.dumps(data), content_type="json")
print(response)
```

### **Delete Customer**

Deletes customer from database.

- **URL**</br>
  /customer/:id
- **Method:**</br>
  `DELETE`
- **URL Parameters:**</br>
  **Required:** </br>
  `id = [integer]`
- **Success Response:**

  - **Code:** 200 </br>
    **Content:** </br>
    `{"code": 200, "message": "Customer id 41 has been successfully deleted."}`

- **Error Response:**

  - **Code:** 400 </br>
    **Content:** </br>
    `{"error": 400, "message": "Invalid Customer ID"}`

- **Sample Call:**

```
import requests
response = requests.get('/customer/41')
print(response)
```
