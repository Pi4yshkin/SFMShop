def validate_age(age):
	return True if age >= 18 else False

def validate_email(email):
	return True if "@" in email and "." in email else False

