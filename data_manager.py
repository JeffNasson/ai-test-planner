from user_generator import create_positive_test_user, create_negative_test_user

def resolve_credentials(case):
    if case["type"] == "positive":
        return create_positive_test_user()
    elif case["type"] == "negative": 
        return create_negative_test_user()
    elif case["type"] == "edge":
        return {
            "username": "",
            "password": ""
        }
    else:
        return {
            "username": "",
            "password": ""
        }
