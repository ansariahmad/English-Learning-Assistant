import re
import json
import requests
from openai import OpenAI

base_url = "https://api.aimlapi.com/v1"

# api key
API_KEY = "970c752628f64a6bb7726afd346c61af"

api = OpenAI(api_key=API_KEY, base_url=base_url)

def get_response(user_prompt: str, frequency_penalty: float = 0.5):
    response = requests.post(
    "https://api.aimlapi.com/v1/chat/completions",
        headers={
            "Content-Type":"application/json",

            # Insert your AIML API Key instead of <YOUR_AIMLAPI_KEY>:
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type":"application/json"
        },
        json={
            "model":"openai/gpt-5-chat-latest",
            "messages":[
                {
                    "role":"user", "content":user_prompt
                }
            ],
            "temperature" : 1.0, "max_tokens" : 2000, "frequency_penalty": frequency_penalty
        }
    )
    return response

def generate_learning_content(learning_topic: str, learning_category: str, learning_subcategory):
    user_prompt = None
    if learning_topic == "Tenses":
        user_prompt = f"""
            You are an English teacher for Pakistani secondary school students (Grades 9–12).  
            The student does not have prior knowledge of English grammar.  

            Task: Explain the **{learning_subcategory} tense** in very simple Urdu.  
            Requirements:  
            - Start with a short introduction of the tense in Urdu.  
            - Show the sentence structure in Urdu + English (e.g., "فاعل + فعل + مفعول") (in form of a table).  
            - Give Urdu-to-English example sentences with translations. Examples should include all type of sentences (simple, negation and questions.). 
            Three examples of each. Examples should be in form of a table.
            - Keep sentences easy, daily-life, and school-level.  
            - Use simple, clear Urdu (avoid technical jargon).  

            Your response should strictly follow the output format. You should not provide any further recommendations. 
            
            Output format:  
            ### {learning_subcategory} Tense  
            **Introduction (Urdu):** ...  
            **Structure:** ...  
            **Examples:**  
            1. Urdu → English  
            2. Urdu → English  
            3. Urdu → English  
            """
        
    elif learning_topic == "Active & Passive Voice":
        user_prompt = f"""
            You are an English teacher for Pakistani secondary school students (Grades 9–12).  

            Task: Teach how to convert sentences from **{learning_category} voice** in the **{learning_subcategory} tense**.  
            Requirements:  
            - Give a short explanation in simple English.  
            - Show the sentence structure (Active → Passive).
            - Provide short example pairs (Active → Passive). Examples should include all type of sentences (simple, negation and questions.). 
            Three examples of each. Examples should be in form of a table.  
            - Keep vocabulary familiar to school-level students.  
            - Keep sentences short (6–10 words).  

            Your response should strictly follow the output format. You should not provide any further recommendations. 

            Output format:  
            ### {learning_subcategory} Tense ({learning_category} Voice)  
            **Explanation:** ...  
            **Structure:** ...  
            **Examples:** 
            """
    elif learning_topic == "Direct & Indirect Speech":
        user_prompt = f"""
            You are an English teacher for Pakistani secondary school students (Grades 9–12).  

            Task: Teach how to convert **{learning_category} speech** sentences in the **{learning_subcategory} tense**.  
            Requirements:  
            - Give a short explanation in simple English.  
            - Show the sentence structure (Direct → Indirect or Indirect → Direct).  
            - Provide example pairs. Examples should include all type of sentences (simple, negation and questions.). 
            Three examples of each. Examples should be in form of a table.   
            - Keep vocabulary familiar to school-level students.  

            Your response should strictly follow the output format. You should not provide any further recommendations. 

            Output format:  
            ### {learning_subcategory} Tense ({learning_category} Speech)  
            **Explanation:** ...  
            **Structure:** ...  
            **Examples:**  
            """

    response = get_response(user_prompt, frequency_penalty=0.5)

    data = response.json()
    output_text = data['choices'][0]['message']['content']
    cleaned = re.sub(r"```(?:json|python)?", "", output_text)
    cleaned = cleaned.strip("` \n")
    # output = json.loads(cleaned)
    return cleaned

def generate_practice_content(topic, category, subcategory, num_questions, difficulty):
    user_prompt = None
    if topic == "Tenses":
        user_prompt = f"""
        You are an English teacher for secondary school students (Grades 9–12).
        Generate {num_questions} Urdu sentences that are all in the **{subcategory} tense**.

        Difficulty Level: {difficulty}
        - Easy: Short and simple daily-life sentences (3–6 words).
        - Medium: Slightly longer (6–9 words), with variations but still easy.
        - Hard: Longer (8–12 words), with uncommon vocabulary.

        Requirements:
        - Sentences should include negations and questions.
        - Sentences must be clear.
        - Use vocabulary familiar to school students.
        - Output strictly as a valid dictionary, following this structure:

        Example:
        {{
        "sentence 1": {{"question" : "urdu text"}},
        "sentence 2": {{"question" : "urdu text"}},
        ...
        }}

        Do not include English translations, explanations, or extra text outside the dictionary.
        """
    else:
        user_prompt = f"""
        You are an English teacher for secondary school students (Grades 9–12).
        Generate {num_questions} English sentences that are all in the **{subcategory} tense** for **{category} conversion**.

        Difficulty Level: {difficulty}
        - Easy: Short and simple daily-life sentences (3–6 words).
        - Medium: Slightly longer (6–9 words), with variations but still easy.
        - Hard: Longer (8–12 words), with uncommon vocabulary.

        Requirements:
        - Sentences should include negations and questions.
        - Sentences must be clear.
        - Use vocabulary familiar to school students.
        - Output strictly as a valid dictionary, following this structure:

        Example:
        {{
        "sentence 1": {{"question" : "text"}},
        "sentence 2": {{"question" : "text"}},
        ...
        }}

        Do not include English translations, explanations, or extra text outside the dictionary.
        """
    response = get_response(user_prompt, frequency_penalty=0.5)
    
    data = response.json()
    output_text = data['choices'][0]['message']['content']
    cleaned = re.sub(r"```(?:json|python)?", "", output_text)
    cleaned = cleaned.strip("` \n")
    output = json.loads(cleaned)
    return output

def evaluate_response(topic, category, subcategory, response: dict):
    user_prompt = f"""
        You are a Pakistani English teacher for secondary school students (Grades 9–12).

        Practice Topic: {topic}
        Practice Category: {category}
        Tense type: {subcategory}
        Content to be Evaluated: {response}

        Instructions for evaluation:
        - Focus mainly on **tense correctness** (verb forms, structure).
        - If the student uses the correct tense but makes **minor errors** (like using "the" unnecessarily, small spelling mistakes, or word order issues), mark it as **Partially correct**, not Incorrect.
        - Always give encouraging and supportive feedback.
        - Keep explanations simple, like a Pakistani teacher guiding school students.

        Tasks:
        1. Evaluate the student's translation as **Correct / Partially correct / Incorrect**.
        2. Provide the correct English translation.
        3. Point out mistakes (only if important for clarity). Ignore very small issues unless they change meaning.
        4. Give short, encouraging feedback (max 2 sentences).

        Response strictly follow the Output Fromat. Response should be appealing for students. Add Emojis if needed.

        Output Format:
        # Evaluation Report
        **Question 01**:
        Question: text
        Your Answer: student_answer
        Actual Answer: actual_answer
        Scoring: number
        ___
        ....
        Feedback: feedback

        Do not include explanations, or extra text outside the Output Format.
        """
    """
    Output Format:
        {{
        "result" : {{"sentence 1": {{"question" : "text", "student answer" : "english", "actual answer" : "english", "scoring" : "number"}}}}
        ...
        "feedback" : "feedback"
        }}
    """

    response = get_response(user_prompt, frequency_penalty=0.2)

    data = response.json()
    output_text = data['choices'][0]['message']['content']
    cleaned = re.sub(r"```(?:json|python)?", "", output_text)
    cleaned = cleaned.strip("` \n")
    # output = json.loads(cleaned)
    return cleaned

def generate_mcqs(topic, category, subcategory, num_questions, difficulty):
    user_prompt = f"""  
    You are an English teacher for secondary school students (Grades 9–12) in Pakistan.

    Generate {num_questions} multiple-choice questions (MCQs) related to **Topic: {topic}**, **Category: {category}** 
    and **Subcategory: {subcategory}**.
    Focus on:
    - Correct form of verbs in sentences.
    - Correct helping verbs (is/are, has/have, had, will, etc.).
    - Correct use of "since" vs. "for" in perfect continuous tense.

    Requirements:
    - Each MCQ must have exactly 1 correct answer and 3 distractors.
    - Provide 4 options labeled (a), (b), (c), (d).
    - Mark the correct option clearly.
    - Use simple vocabulary suitable for Grade 9–12 students.
    - Each MCQ only contains one blank.
    - Output strictly as a valid Python dictionary in the following format:

    {{
      "MCQ 1": {{
        "question": "question text here",
        "options": {{
          "a": "option text",
          "b": "option text",
          "c": "option text",
          "d": "option text"
        }},
        "answer": "correct option text"
      }},
      ...
    }}
    Do not include English translations, explanations, or extra text outside the dictionary.

"""
    response = get_response(user_prompt, frequency_penalty=0.0)
    
    data = response.json()
    output_text = data['choices'][0]['message']['content']
    cleaned = re.sub(r"```(?:json|python)?", "", output_text)
    cleaned = cleaned.strip("` \n")
    print(cleaned)
    output = json.loads(cleaned)
    return output