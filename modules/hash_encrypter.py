import bcrypt


# Function to hash a password with a salt
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


# Function to check a password against a hashed password
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)


