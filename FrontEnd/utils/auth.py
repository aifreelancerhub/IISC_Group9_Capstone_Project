# utils/auth.py
import streamlit as st
import yaml
import streamlit_authenticator as stauth
import os

class Authentication:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config/auth_config.yaml')
        with open(config_path) as file:
            self.config = yaml.safe_load(file)

        self.authenticator = stauth.Authenticate(
            credentials=self.config['credentials'],
            cookie_name=self.config['cookie']['name'],
            key=self.config['cookie']['key'],
            cookie_expiry_days=self.config['cookie']['expiry_days']
        )

    def authenticate(self):
        try:
            login_status = self.authenticator.login(
                fields=['username', 'password'],
                location='main'
            )

            if login_status:
                if st.session_state["authentication_status"]:
                    return (
                        st.session_state["name"], 
                        st.session_state["authentication_status"], 
                        st.session_state["username"]
                    )
                elif st.session_state["authentication_status"] is False:
                    st.error('Username/password is incorrect')
                    return None, False, None
                elif st.session_state["authentication_status"] is None:
                    st.warning('Please enter your username and password')
                    return None, None, None
            
            return None, None, None
        
        except Exception as e:
            st.error(f"An error occurred during authentication: {e}")
            return None, None, None

    def logout(self):
        self.authenticator.logout('Logout', 'main', key='unique_key')

import bcrypt
import yaml

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

passwords = {
    'admin': 'admin_password',
    'advisor': 'advisor_password',
    'analyst': 'analyst_password'
}

config_path = os.path.join(os.path.dirname(__file__), '../config/auth_config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

for username in config['credentials']['usernames']:
    if username in passwords:
        config['credentials']['usernames'][username]['password'] = hash_password(passwords[username])

with open(config_path, 'w') as file:
    yaml.dump(config, file)

print("Passwords updated successfully!")
