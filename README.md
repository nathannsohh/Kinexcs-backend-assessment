# Kinexcs Backend Assessment

## Technology

Flask, Marshmallow, SQLAlchemy, POSTGRESQL

## API Endpoints

## **Get Customers**

Returns json data about all the customers.

- **URL**</br>
  /customer
- **Method:**</br>
  `GET`
- **URL Parameters:**
  None
- **Success Response:**
  - **Code:** 200 </br>
    **Content:** `{{"id": 1, name: "John Tan", "dob": "1999-03-29"}, {"id": 2, "name": "Jane Doe", "dob": "1987-11-05"}, ...}`
- **Error Response:**
  None
- **Sample Call:**

```
import requests
response = requests.get('/customer')
print(response)
```
