# shopping_master
Based On Python 3.10
Django 4.0.3
#Steps to Run Project
## Create a VirtualEnv
```virtualenv -p python3.10 venv```

## Install Dependencies
```pip install -r requirements/staging.txt```

## Import Postman Collection
## Note:
Everything is based on JWT Authentication
But is mandatory to send a valid JWT token in Header


##Tasks:
1. Create user signup for crud operation create,update.

2. Create user login API  with  two factor authentication with 6 digit otp .(you can take otp static value )

3. Create a product management system :--

    For this there are 3 types of users and each user have their own permissions:

    1 user :: Can update, delete, read and publish products

    2 user :: Update, create and read products

    3 user  :: Read and create products

 

Now, create API for
a. Add product API (For this take fields- Product Name, Product price, discount price, Product fabric type, Colour, sizes (XS, S, M, L, XL) and product description)

    update product API

    delete product API

    Fetch product List from db API

    product description.

    product publish or unpublish API.
b. Create system for bulk upload of product via excel sheet. For product upload use these filed options: Product Name, Product price, discount price, Product fabric type, Colour, sizes (XS, S, M, L, XL) and product description

```One product can be available in different colours so treat them like child.```


## All Task are Complete except Permission Related due to time Constraint.
###```One product can be available in different colours so treat them like child.```
Wasnt able to understand the task. sent mail to clarification but didnt got the reply
