import random

# Simulate API create user function. In an enterprise application we want to do this via internal API and send credentials securely
def create_positive_test_user():
    return {
        "username": "tomsmith",
        "password": "SuperSecretPassword!"
    }

def create_negative_test_user():
    return {
        "username": f"invalid{random.randint(1000,9999)}",
        "password": "WrongPassword!"
    }