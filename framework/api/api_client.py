import random

def create_api_user(valid = True):
    print(f"[API] Creating {'valid' if valid else 'invalid'} user...")
    """
    Simulate API create user function. In an enterprise application we want to do this via internal API and send credentials securely
    
    """

    # Simulating a POST to /users endpoint and handling the response object.
    if valid:
        return {
            "username": "tomsmith",
            "password": "SuperSecretPassword!",
            "status": 201
        }
    else:
        return {
            "username": f"invalid{random.randint(1000,9999)}",
            "password": "WrongPassword!",
            "status": 401
        }