import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['capstone', 'pepepw', 'gustavopw']).generate()
print(hashed_passwords)
