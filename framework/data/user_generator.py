from framework.api.api_client import create_api_user

# Simulate API create user function. In an enterprise application we want to do this via internal API and send credentials securely
def create_positive_test_user():
    response = create_api_user(valid=True)
    return {
        "username": response["username"],
        "password": response["password"]
    }

def create_negative_test_user():
    response = create_api_user(valid=False)
    return {
        "username": response["username"],
        "password": response["password"]
    }