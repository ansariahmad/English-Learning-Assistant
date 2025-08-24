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

from utils import generate_mcqs

# Page configuration
st.set_page_config(page_title="MCQs Drill - English Assistant", page_icon="💪")

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
if 'mcq_topic' not in st.session_state:
    st.session_state.mcq_topic = None
if 'mcq_category' not in st.session_state:
    st.session_state.mcq_category = None
if 'mcq_subcategory' not in st.session_state:
    st.session_state.mcq_subcategory = None
if 'question_num' not in st.session_state:
    st.session_state.question_num = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = None
if 'mcq_questions' not in st.session_state:
    st.session_state.mcq_questions = []
if 'mcq_content' not in st.session_state:
    st.session_state['mcq_content'] = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = list()
if 'evaluation_report' not in st.session_state:
    st.session_state['evaluation_report'] = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Main content
st.title("📖 MCQ Section")
st.markdown("mcq English grammar concepts")

# Topic selection
st.subheader("Step 1: Choose what you want to MCQ")
topics = ["Select a topic", "Tenses", "Active & Passive Voice", "Direct & Indirect Speech"]
selected_topic = st.selectbox("📚 Select MCQ Topic:", topics)

if selected_topic != "Select a topic":
    st.session_state.mcq_topic = selected_topic
    
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
            st.session_state.mcq_category = "Tense"
            st.session_state.mcq_subcategory = selected_tense
    
    elif selected_topic == "Active & Passive Voice":
        st.subheader("Step 2: Choose conversion type")
        conversion_types = ["Select conversion", "Active to Passive", "Passive to Active"]
        selected_conversion = st.selectbox("🔄 Select Conversion Type:", conversion_types)
        
        if selected_conversion != "Select conversion":
            st.session_state.mcq_category = selected_conversion
            
            st.subheader("Step 3: Choose the tense")
            tense_types = [
                "Select tense",
                "Simple Present", "Simple Past", "Simple Future",
                "Present Continuous", "Past Continuous",
                "Present Perfect", "Past Perfect"
            ]
            selected_tense = st.selectbox("⏰ Select Tense for Voice:", tense_types)
            
            if selected_tense != "Select tense":
                st.session_state.mcq_subcategory = selected_tense
    
    elif selected_topic == "Direct & Indirect Speech":
        st.subheader("Step 2: Choose conversion type")
        speech_types = ["Select conversion", "Direct to Indirect", "Indirect to Direct"]
        selected_speech = st.selectbox("💬 Select Speech Conversion:", speech_types)
        
        if selected_speech != "Select conversion":
            st.session_state.mcq_category = selected_speech
            
            st.subheader("Step 3: Choose the tense")
            tense_types = [
                "Select tense",
                "Simple Present", "Simple Past", "Simple Future",
                "Present Continuous", "Past Continuous",
                "Present Perfect"
            ]
            selected_tense = st.selectbox("⏰ Select Tense for Speech:", tense_types)
            
            if selected_tense != "Select tense":
                st.session_state.mcq_subcategory = selected_tense
    

# Generate and display content
if (st.session_state.mcq_topic and 
    st.session_state.mcq_category and 
    st.session_state.mcq_subcategory):

    st.subheader("Choose number of questions to MCQ")
    num_examples = st.slider("No. of Questions... ", 1, 15, 5)
    st.session_state.question_num = num_examples
    
    st.markdown("---")
    
    
    if user_data['grade'] == "Grade 9":
        st.session_state.difficulty = "Easy"
    elif user_data['grade'] == "Grade 10":
        st.session_state.difficulty = "Medium"
    else:
        st.session_state.difficulty = "Difficult"
    
    if st.button("📖 Generate MCQ Content", type="primary"):
        with st.spinner("Generating your MCQ content..."):
            content = generate_mcqs(
                st.session_state.mcq_topic,
                st.session_state.mcq_category,
                st.session_state.mcq_subcategory,
                st.session_state.question_num,
                st.session_state.difficulty
            )
            st.session_state['mcq_content'] = content
    
if st.session_state['mcq_content']:
    st.success("Content generated successfully!")
    with st.container(border=True):
        for key in st.session_state['mcq_content']:
            option = st.radio(label=st.session_state['mcq_content'][key]['question'],
                            options=[st.session_state['mcq_content'][key]['options']['a'], st.session_state['mcq_content'][key]['options']['b'],
                                        st.session_state['mcq_content'][key]['options']['c'], st.session_state['mcq_content'][key]['options']['d']],
                                        index=None)
            if option == st.session_state['mcq_content'][key]['answer']:
                st.write(":green[Correct Answer!]") 
            elif option == None:
                pass
            else:
                st.write(":red[Incorrect Answer]")
    
# Progress tracking
if st.session_state.mcq_topic:
    st.sidebar.markdown("### 📊 Your Progress")
    st.sidebar.markdown(f"**Topic:** {st.session_state.mcq_topic}")
    if st.session_state.mcq_category:
        st.sidebar.markdown(f"**Category:** {st.session_state.mcq_category}")
    if st.session_state.mcq_subcategory:
        st.sidebar.markdown(f"**Subcategory:** {st.session_state.mcq_subcategory}")

# Help section
with st.sidebar:
    st.markdown("### 💡 MCQ Solving Tips")
    st.info("""
    **How to approach MCQs:**
    - Read the question carefully  
    - Eliminate obviously wrong options  
    - Watch out for tricky wording  
    - Don’t rush, but manage time wisely  
    - Review your marked answers if possible  
    """)

    st.markdown("### 🎯 MCQ Focus Areas")
    st.warning("""
    **For Grammar MCQs:**
    - Pay attention to verb tenses  
    - Identify subject–verb agreement  
    - Watch sentence voice (active/passive)  
    - Check direct vs. indirect speech  
    - Spot the correct prepositions & articles  
    """)
