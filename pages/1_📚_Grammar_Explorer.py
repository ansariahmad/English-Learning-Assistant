import os
import sys
import streamlit as st

cwd = os.getcwd()
cwd = cwd.split("\\")[:-1]
cwd.append("utils.py")
path = os.path.join("\\".join(cwd))
project_root = os.path.dirname(os.path.abspath(path))
sys.path.insert(0, project_root)

from utils import generate_learning_content

# Page configuration
st.set_page_config(page_title="Learning - English Assistant", page_icon="📖")

# Authentication check
if not st.session_state.get('logged_in', False):
    st.error("🔐 Please login to access this page!")
    if st.button("🏠 Go to Login Page"):
        st.switch_page("app.py")
    st.stop()

# Display user info in header
if st.session_state.get('username'):
    st.markdown(f"**👤 Welcome, {st.session_state.username}!**")
    st.markdown("---")

# Initialize session states
if 'learning_topic' not in st.session_state:
    st.session_state.learning_topic = None
if 'learning_category' not in st.session_state:
    st.session_state.learning_category = None
if 'learning_subcategory' not in st.session_state:
    st.session_state.learning_subcategory = None
if 'learning_content' not in st.session_state:
    st.session_state['learning_content'] = None

# Main content
st.title("📖 Learning Section")
st.markdown("Learn English grammar concepts step by step")

# Topic selection
st.subheader("Step 1: Choose what you want to learn")
topics = ["Select a topic", "Tenses", "Active & Passive Voice", "Direct & Indirect Speech"]
selected_topic = st.selectbox("📚 Select Learning Topic:", topics)

if selected_topic != "Select a topic":
    st.session_state.learning_topic = selected_topic
    
    # Category selection based on topic
    if selected_topic == "Tenses":
        st.subheader("Step 2: Choose the tense type")
        tense_types = [
            "Select tense type",
            "Simple Present", "Present Continuous", "Present Perfect", "Present Perfect Continuous",
            "Simple Past", "Past Continuous", "Past Perfect", "Past Perfect Continuous",
            "Simple Future", "Future Continuous", "Future Perfect", "Future Perfect Continuous"
        ]
        selected_tense = st.selectbox("⏰ Select Tense Type:", tense_types)
        
        if selected_tense != "Select tense type":
            st.session_state.learning_category = "Tense"
            st.session_state.learning_subcategory = selected_tense
    
    elif selected_topic == "Active & Passive Voice":
        st.subheader("Step 2: Choose conversion type")
        conversion_types = ["Select conversion", "Active to Passive", "Passive to Active"]
        selected_conversion = st.selectbox("🔄 Select Conversion Type:", conversion_types)
        
        if selected_conversion != "Select conversion":
            st.session_state.learning_category = selected_conversion
            
            st.subheader("Step 3: Choose the tense")
            tense_types = [
                "Select tense",
                "Simple Present", "Simple Past", "Simple Future",
                "Present Continuous", "Past Continuous",
                "Present Perfect", "Past Perfect"
            ]
            selected_tense = st.selectbox("⏰ Select Tense for Voice:", tense_types)
            
            if selected_tense != "Select tense":
                st.session_state.learning_subcategory = selected_tense
    
    elif selected_topic == "Direct & Indirect Speech":
        st.subheader("Step 2: Choose conversion type")
        speech_types = ["Select conversion", "Direct to Indirect", "Indirect to Direct"]
        selected_speech = st.selectbox("💬 Select Speech Conversion:", speech_types)
        
        if selected_speech != "Select conversion":
            st.session_state.learning_category = selected_speech
            
            st.subheader("Step 3: Choose the tense")
            tense_types = [
                "Select tense",
                "Simple Present", "Simple Past", "Simple Future",
                "Present Continuous", "Past Continuous",
                "Present Perfect"
            ]
            selected_tense = st.selectbox("⏰ Select Tense for Speech:", tense_types)
            
            if selected_tense != "Select tense":
                st.session_state.learning_subcategory = selected_tense

# Generate and display content
if (st.session_state.learning_topic and 
    st.session_state.learning_category and 
    st.session_state.learning_subcategory):
    
    st.markdown("---")
    
    if st.button("📖 Generate Learning Content", type="primary"):
        with st.spinner("Generating your learning content..."):
            content = generate_learning_content(
                st.session_state.learning_topic,
                st.session_state.learning_category,
                st.session_state.learning_subcategory
            )
            st.session_state['learning_content'] = content
    
if st.session_state['learning_content']:
    st.success("Content generated successfully!")
    with st.container(border=True):
        st.markdown(st.session_state['learning_content'])
        st.download_button(
            label="📥 Download as Markdown",
            data=st.session_state['learning_content'],
            file_name=f"{st.session_state.learning_subcategory}.md",
            mime="text/markdown"
            )

# Progress tracking
if st.session_state.learning_topic:
    st.sidebar.markdown("### 📊 Your Progress")
    st.sidebar.markdown(f"**Topic:** {st.session_state.learning_topic}")
    if st.session_state.learning_category:
        st.sidebar.markdown(f"**Category:** {st.session_state.learning_category}")
    if st.session_state.learning_subcategory:
        st.sidebar.markdown(f"**Subcategory:** {st.session_state.learning_subcategory}")

# Help section
with st.sidebar:
    st.markdown("### 💡 Learning Tips")
    st.info("""
    **Effective Learning:**
    - Read the explanation carefully
    - Pay attention to examples
    - Note the common mistakes
    - Practice immediately after learning
    - Review regularly
    """)
    
    st.markdown("### 🎯 Focus Areas")
    st.warning("""
    **For Pakistani Students:**
    - Focus on sentence structure
    - Practice with Urdu examples
    - Understand the context
    - Use in daily conversation
    """)