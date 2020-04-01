from werkzeug.security import generate_password_hash, check_password_hash


if __name__ == "__main__":
    password = '123456'
    password_hash = generate_password_hash(password)
    print(password_hash)

    valid = check_password_hash(password_hash, password)
    print(valid)