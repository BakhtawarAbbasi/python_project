import streamlit as st

class Resume:
    def __init__(self, owner_username):
        self.owner = owner_username
        self.personal_info = {
            "full_name": "",
            "email": "",
            "phone": "",
            "summary": ""
        }

    def update_personal_info(self, full_name, email, phone, summary):
        self.personal_info["full_name"] = full_name
        self.personal_info["email"] = email
        self.personal_info["phone"] = phone
        self.personal_info["summary"] = summary

    def display_personal_info(self):
        return f"""
**Name:** {self.personal_info['full_name']}

**Email:** {self.personal_info['email']}

**Phone:** {self.personal_info['phone']}

**Summary:** {self.personal_info['summary']}
"""

if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {}

if 'resumes' not in st.session_state:
    st.session_state['resumes'] = {}

def signup():
    st.subheader("Create new account")
    new_username = st.text_input("Username", key="signup_username")
    new_email = st.text_input("Email", key="signup_email")
    new_password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if new_username in st.session_state['users_db']:
            st.error("Username already exists!")
        elif not new_username or not new_email or not new_password:
            st.error("Please fill all fields.")
        else:
            st.session_state['users_db'][new_username] = {"email": new_email, "password": new_password}
            st.success("Account created! Please login.")

def login():
    st.subheader("Login to ResumeForge")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        user = st.session_state['users_db'].get(username)
        if user and user["password"] == password:
            st.success(f"Welcome back, {username}!")
            st.session_state['logged_in_user'] = username
            # Instead of experimental_rerun, stop execution to trigger rerun
            st.experimental_rerun = None  # disable any accidental use
            st.stop()  # stops execution and triggers rerun automatically
        else:
            st.error("Invalid username or password.")

def personal_info_form(username):
    st.subheader("Add Your Personal Info")
    if username not in st.session_state['resumes']:
        st.session_state['resumes'][username] = Resume(username)

    resume = st.session_state['resumes'][username]

    full_name = st.text_input("Full Name", value=resume.personal_info["full_name"])
    email = st.text_input("Email", value=resume.personal_info["email"])
    phone = st.text_input("Phone Number", value=resume.personal_info["phone"])
    summary = st.text_area("Professional Summary", value=resume.personal_info["summary"])

    if st.button("Save Personal Info"):
        if not full_name or not email:
            st.error("Name and Email are required.")
        else:
            resume.update_personal_info(full_name, email, phone, summary)
            st.success("Personal info saved!")

    st.markdown("### Preview:")
    st.markdown(resume.display_personal_info())

def main():
    st.title("🔥 ResumeForge 🔥")

    if "logged_in_user" not in st.session_state:
        option = st.radio("Choose Action:", ["Login", "Sign Up"])
        if option == "Login":
            login()
        else:
            signup()
    else:
        username = st.session_state['logged_in_user']
        st.write(f"Welcome, **{username}**! You are logged in.")
        personal_info_form(username)

        if st.button("Logout"):
            del st.session_state['logged_in_user']
            # Use st.stop() to simulate rerun after logout
            st.stop()

if __name__ == "__main__":
    main()
