import os
import sys
import streamlit as st
from datetime import datetime

cwd = os.getcwd()
cwd = cwd.split("\\")[:-1]
cwd.append("utils.py")
path = os.path.join("\\".join(cwd))
project_root = os.path.dirname(os.path.abspath(path))
sys.path.insert(0, project_root)

from utils import generate_practice_content, evaluate_response

# Page configuration
st.set_page_config(page_title="Practice - English Assistant", page_icon="💪")

# Authentication check
if not st.session_state.get('logged_in', False):
    st.error("🔐 Please login to access this page!")
    if st.button("🏠 Go to Login Page"):
        st.switch_page("app.py")
    st.stop()

# Display user info in header
if st.session_state.get('username'):
    user_data = st.session_state.users_db[st.session_state.username]
    st.markdown(f"**👤 Welcome, {st.session_state.username}!**")
    st.markdown("---")

# Initialize session states
if 'practice_topic' not in st.session_state:
    st.session_state.practice_topic = None
if 'practice_category' not in st.session_state:
    st.session_state.practice_category = None
if 'practice_subcategory' not in st.session_state:
    st.session_state.practice_subcategory = None
if 'question_num' not in st.session_state:
    st.session_state.question_num = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = None
if 'practice_questions' not in st.session_state:
    st.session_state.practice_questions = []
if 'practice_content' not in st.session_state:
    st.session_state['practice_content'] = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = list()
if 'evaluation_report' not in st.session_state:
    st.session_state['evaluation_report'] = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Main content
st.title("📖 Practice Section")
st.markdown("Practice English grammar concepts")

# Topic selection
st.subheader("Step 1: Choose what you want to practice")
topics = ["Select a topic", "Tenses", "Active & Passive Voice", "Direct & Indirect Speech"]
selected_topic = st.selectbox("📚 Select Practice Topic:", topics)

if selected_topic != "Select a topic":
    st.session_state.practice_topic = selected_topic
    
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
            st.session_state.practice_category = "Tense"
            st.session_state.practice_subcategory = selected_tense
    
    elif selected_topic == "Active & Passive Voice":
        st.subheader("Step 2: Choose conversion type")
        conversion_types = ["Select conversion", "Active to Passive", "Passive to Active"]
        selected_conversion = st.selectbox("🔄 Select Conversion Type:", conversion_types)
        
        if selected_conversion != "Select conversion":
            st.session_state.practice_category = selected_conversion
            
            st.subheader("Step 3: Choose the tense")
            tense_types = [
                "Select tense",
                "Simple Present", "Simple Past", "Simple Future",
                "Present Continuous", "Past Continuous",
                "Present Perfect", "Past Perfect"
            ]
            selected_tense = st.selectbox("⏰ Select Tense for Voice:", tense_types)
            
            if selected_tense != "Select tense":
                st.session_state.practice_subcategory = selected_tense
    
    elif selected_topic == "Direct & Indirect Speech":
        st.subheader("Step 2: Choose conversion type")
        speech_types = ["Select conversion", "Direct to Indirect", "Indirect to Direct"]
        selected_speech = st.selectbox("💬 Select Speech Conversion:", speech_types)
        
        if selected_speech != "Select conversion":
            st.session_state.practice_category = selected_speech
            
            st.subheader("Step 3: Choose the tense")
            tense_types = [
                "Select tense",
                "Simple Present", "Simple Past", "Simple Future",
                "Present Continuous", "Past Continuous",
                "Present Perfect"
            ]
            selected_tense = st.selectbox("⏰ Select Tense for Speech:", tense_types)
            
            if selected_tense != "Select tense":
                st.session_state.practice_subcategory = selected_tense
    

# Generate and display content
if (st.session_state.practice_topic and 
    st.session_state.practice_category and 
    st.session_state.practice_subcategory):

    st.subheader("Choose number of questions to practice")
    num_examples = st.slider("No. of Questions... ", 1, 15, 5)
    st.session_state.question_num = num_examples
    
    st.markdown("---")
    
    
    if user_data['grade'] == "Grade 9":
        st.session_state.difficulty = "Easy"
    elif user_data['grade'] == "Grade 10":
        st.session_state.difficulty = "Medium"
    else:
        st.session_state.difficulty = "Difficult"
    
    if st.button("📖 Generate Practice Content", type="primary"):
        with st.spinner("Generating your Practice content..."):
            content = generate_practice_content(
                st.session_state.practice_topic,
                st.session_state.practice_category,
                st.session_state.practice_subcategory,
                st.session_state.question_num,
                st.session_state.difficulty
            )
            st.session_state['practice_content'] = content
    
if st.session_state['practice_content']:
    st.session_state.practice_questions = []
    st.session_state.user_answers = []
    st.success("Content generated successfully!")
    with st.container(border=True):
        for key1 in st.session_state['practice_content']:
            st.markdown(st.session_state['practice_content'][key1]['question'])
            st.session_state.practice_questions.append(st.session_state['practice_content'][key1]['question'])
            user_answer = st.text_input(label=f"Translate {st.session_state['practice_content'][key1]['question']}", max_chars=100)
            st.session_state['practice_content'][key1]['student answer'] = user_answer

if st.button('Evaluate Your Response'):
    with st.spinner("Evaluating Your Response..."):
        output = evaluate_response(st.session_state.practice_topic, st.session_state.practice_category, st.session_state.practice_subcategory, 
                               st.session_state['practice_content'])
        st.session_state['evaluation_report'] = output
    
if st.session_state['evaluation_report'] is not None:
    with st.container(border=True):
        st.markdown(st.session_state['evaluation_report'])
    
# Progress tracking
if st.session_state.practice_topic:
    st.sidebar.markdown("### 📊 Your Progress")
    st.sidebar.markdown(f"**Topic:** {st.session_state.practice_topic}")
    if st.session_state.practice_category:
        st.sidebar.markdown(f"**Category:** {st.session_state.practice_category}")
    if st.session_state.practice_subcategory:
        st.sidebar.markdown(f"**Subcategory:** {st.session_state.practice_subcategory}")

# Help section
with st.sidebar:
    st.markdown("### 💡 Practice Tips")
    st.info("""
    **How to practice effectively:**
    - Start with simple examples  
    - Repeat exercises for better retention  
    - Compare your answers with solutions  
    - Focus on one topic at a time  
    - Track your progress regularly  
    """)

    st.markdown("### 🎯 Practice Focus Areas")
    st.warning("""
    **For Grammar Practice:**
    - Build strong basics of tenses  
    - Practice active ↔ passive conversions  
    - Try direct ↔ indirect speech exercises  
    - Apply practice in your daily writing & speaking  
    """)
