def main():
# # Imports
# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO  



# # Set up our App
# st.set_page_config(page_title="Data Sweeper", layout="wide", page_icon=":fire:")
# st.title("💿 Data Sweeper")
# st.write("Transform your files between CSV and Excel formats with buit-in data cleaning and visualization!")

# uploaded_files = st.file_uploader("Upload your files (CSV or Excel) : ", type=["csv", "xlsx"] , accept_multiple_files=True)

# if uploaded_files :
#     for file in uploaded_files :
#         file_ext = os.path.splitext(file.name)[-1].lower()
# a
#         if file_ext == ".csv" :
#             df = pd.read_csv(file)
#         elif file_ext == ".xlsx" :
#             df = pd.read_excel(file)
#         else :
#             st.error(f"Unsupported file type : {file_ext}")
#             continue

#         # st.write(df.head())
#       # Diplsay info about the file
#         st.write(f"**File Name :** {file.name}")
#         st.write(f"**File Size : ** {file.size/1024}")

#         # Show 5 rows of our df
#         st.write("Preview of the Head of the Data Frame")
#         st.dataframe(df.head())


    import streamlit as st
    import json
    import os

    st.set_page_config(
        page_title="Growth Mind Set",
        page_icon = ":cd:",
        layout = "centered"
    )

    def load_user_data(username):
        try:
            with open(f'users/{username}.json', 'r') as f:
                return json.load(f)
        except:
            return None

    # Add tabs for Sign Up and Login
    tab1, tab2 = st.tabs(["Sign Up", "Login"])

    def save_user_data(username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }
        if not os.path.exists('users'):
            os.makedirs('users')
        with open(f'users/{username}.json', 'w') as f:
            json.dump(user_data, f)

    with tab1:
        st.title("Sign Up To Growth Mind")
        name = st.text_input("Enter username : ", key="signup_name")
        email = st.text_input("Enter email : ", key="signup_email")
        password = st.text_input("Enter password : ", type="password", key="signup_password")

        if st.button("Sign Up"):
            if name and email and password:
                if "@" in email and "." in email:
                    if len(password) >= 6:
                        # Save user data
                        save_user_data(name, email, password)
                        st.success("Account created successfully!")
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = name
                        st.switch_page("pages/app.py")
                    else:
                        st.error("Password must be at least 6 characters long")
                else:
                    st.error("Please enter a valid email address")
            else:
                st.error("Please fill in all fields")

    with tab2:
        st.title("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_username and login_password:
                user_data = load_user_data(login_username)
                if user_data and user_data['password'] == login_password:
                    st.success("Login successful!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = login_username
                    st.switch_page("pages/app.py")
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")

        
        



if __name__ == "__main__":
    main()
