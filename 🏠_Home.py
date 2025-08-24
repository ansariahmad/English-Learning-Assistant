import hashlib
import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="English Learning Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if 'learning_topic' not in st.session_state:
    st.session_state.learning_topic = None
if 'learning_category' not in st.session_state:
    st.session_state.learning_category = None
if 'learning_subcategory' not in st.session_state:
    st.session_state.learning_subcategory = None
if 'practice_data' not in st.session_state:
    st.session_state.practice_data = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}  # Simple in-memory user database

# User authentication functions
def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

st.session_state.users_db["guest"] = {
    "password": hash_password('123456'),
    "email": "guest@gmail.com",
    "grade": "Grade 9",
    "created_date": datetime.now().isoformat(),
    "practice_sessions": 0,
    "learning_sessions": 0
}

def sign_up_user(username, password, email, grade):
    """Register a new user"""
    if username in st.session_state.users_db:
        return False, "Username already exists!"
    
    st.session_state.users_db[username] = {
        "password": hash_password(password),
        "email": email,
        "grade": grade,
        "created_date": datetime.now().isoformat(),
        "practice_sessions": 0,
        "learning_sessions": 0
    }
    return True, "Account created successfully!"

def sign_in_user(username, password):
    """Authenticate user"""
    # if username not in st.session_state.users_db:
    #     return False, "Username not found!"
    
    # if st.session_state.users_db[username]["password"] != hash_password(password):
    #     return False, "Invalid password!"
    
    st.session_state.logged_in = True
    st.session_state.username = "guest"
    return True, "Login successful!"

def logout_user():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.show_signup = False

def show_auth_form():
    """Display authentication form"""
    st.markdown("### 🔐 User Authentication")
    
    # Auth container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Auth mode selection
            auth_col1, auth_col2 = st.columns(2)
            
            with auth_col1:
                if st.button("📝 Sign Up", type="secondary", use_container_width=True):
                    st.session_state.show_signup = True
            
            with auth_col2:
                if st.button("🔑 Sign In", type="primary", use_container_width=True):
                    st.session_state.show_signup = False
            
            st.markdown("---")
            
            # Sign Up Form
            if st.session_state.show_signup:
                st.markdown("#### Create New Account")
                
                with st.form("signup_form"):
                    new_username = st.text_input("Username*", placeholder="Enter your username", icon="👤")
                    new_email = st.text_input("Email*", placeholder="Enter your email", icon="📧")
                    new_password = st.text_input("Password*", type="password", placeholder="Create a password", icon="🔒")
                    confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password",
                                                     icon="🔒")
                    
                    grade_options = ["Select Grade", "Grade 9", "Grade 10", "Grade 11", "Grade 12"]
                    selected_grade = st.selectbox("Select Your Grade*", grade_options)
                    
                    signup_submitted = st.form_submit_button("📝 Create Account", type="primary")
                    
                    if signup_submitted:
                        if not all([new_username, new_email, new_password, confirm_password]) or selected_grade == "Select Grade":
                            st.error("Please fill all required fields!")
                        elif new_password != confirm_password:
                            st.error("Passwords don't match!")
                        elif len(new_password) < 5:
                            st.error("Password must be at least 5 characters long!")
                        else:
                            success, message = sign_up_user(new_username, new_password, new_email, selected_grade)
                            if success:
                                st.success(message)
                                st.session_state.show_signup = False
                                st.balloons()
                            else:
                                st.error(message)
            
            # Sign In Form
            else:
                st.markdown("#### Sign In to Your Account")
                
                with st.form("signin_form"):
                    username = st.text_input("Username", placeholder="Enter your username", value="guest", icon="👤")
                    password = st.text_input("Password", type="password", placeholder="Enter your password", value="123456",
                                             icon="🔒")
                    
                    signin_submitted = st.form_submit_button("🔑 Sign In", type="primary")
                    
                    if signin_submitted:
                        if not username or not password:
                            st.error("Please enter both username and password!")
                        else:
                            success, message = sign_in_user(username, password)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
            
            # Switch between forms
            if st.session_state.show_signup:
                st.markdown("Already have an account? Click **Sign In** above")
            else:
                st.markdown("Don't have an account? Click **Sign Up** above")

# Main page content
def main():
    # Check if user is logged in
    if not st.session_state.logged_in:
        # Show authentication form
        st.title("🎓 English Learning Assistant")
        st.subheader("Welcome! Please sign in or create an account to continue")
        
        show_auth_form()
        
        # Brief app description for non-logged users
        st.markdown("---")
        st.markdown("### About This App")
        st.info("""
        📚 **AI-Powered English Learning** designed specifically for Pakistani students (Grades 9-12)
        
        **Features:**
        - Interactive Grammar Learning (Tenses, Voice, Speech)
        - Practice Exercises with Instant Feedback
        - Essay Writing Assistance
        - Upload Your Own Materials
        - Progress Tracking
        """)
        
        return
    
    # User is logged in - show main content
    user_data = st.session_state.users_db[st.session_state.username]
    
    # User info box in sidebar
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        with st.container():
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='margin: 0; color: #1f77b4;'>👋 Welcome!</h4>
                <p style='margin: 5px 0;'><strong>Name:</strong> {st.session_state.username}</p>
                <p style='margin: 5px 0;'><strong>Grade:</strong> {user_data['grade']}</p>
                <p style='margin: 5px 0;'><strong>Practice Sessions:</strong> {user_data['practice_sessions']}</p>
                <p style='margin: 5px 0;'><strong>Learning Sessions:</strong> {user_data['learning_sessions']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                logout_user()
                st.rerun()
    
    # Header with user greeting
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title("🎓 English Learning Assistant")
        st.subheader(f"Welcome back, {st.session_state.username}! 👋")
    
    with col3:
        # User greeting box
        st.markdown(f"""
        <div style='text-align: right; padding: 10px; background-color: #e8f4fd; border-radius: 8px; margin-top: 10px;'>
            <strong>🎓 {user_data['grade']} Student</strong><br>
            <small>Ready to learn today?</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Welcome section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0;'>
            <h3>📚 Welcome to Your English Learning Journey!</h3>
            <p>This application is designed specifically for Pakistani students to improve their English language skills using AI technology in a controlled and educational environment.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("### 🌟 What You Can Do Here:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📖 Learning Section:**
        - Learn Tenses (Past, Present, Future)
        - Master Active & Passive Voice
        - Understand Direct & Indirect Speech
        - Get detailed explanations with examples
        """)
    
    with col2:
        st.markdown("""
        **📝 Practice Section:**
        - Practice with real examples
        - Get instant feedback
        - Download detailed reports
        - Track your progress
        """)
    
    with col3:
        st.markdown("""
        **✍️ MCQ Practice:**
        - Practice form of verbs and helping verbs
        - Practice different tenses
        """)
    
    # Quick start guide
    st.markdown("---")
    st.markdown("### 🚀 How to Get Started:")
    
    steps_col1, steps_col2, steps_col3 = st.columns(3)
    
    with steps_col1:
        st.markdown("""
        **Step 1** 📖
        
        Start with the **Grammar_Explorer** section to understand concepts
        """)
    
    with steps_col2:
        st.markdown("""
        **Step 2** 💪
        
        Practice what you learned in the **Language_Playground** section
        """)
    
    with steps_col3:
        st.markdown("""
        **Step 3** ✍️
        
        Improve your grammar in **MCQ_Drill**
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #666; margin-top: 50px;'>
        <p>🎯 <strong>Focus on Learning:</strong> This app is designed to keep you focused on educational content</p>
        <p>🇵🇰 Made for Pakistani Students | Grades 9-12</p>
        <p>👤 Currently logged in as: <strong>{st.session_state.username}</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()