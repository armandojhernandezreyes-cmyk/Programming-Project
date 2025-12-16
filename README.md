# Python + Streamlit Web Application  
## Login System · SQLite Database · Google OAuth · Text Summarizer · Chatbot UI

---

## 📌 Project Description
### Overview
This project is a Streamlit web application built using Python.  
It demonstrates user authentication, database management using SQLite, and simple Generative AI features.

### Purpose
- Learn backend basics with Python  
- Implement secure user authentication  
- Store and manage users using SQLite  
- Integrate basic AI features  
- Deploy a working web application  

---

## 📌 How the Assignment Was Implemented

### 🔐 Authentication System
#### Email and Password Login
- Users can sign up using an email and password  
- Users can log in using their credentials  
- A logout button is provided  
- A forgot password feature allows password reset  

#### Security Measures
- Passwords are hashed using bcrypt  
- Plain text passwords are never stored  
- Login state is managed using `st.session_state`  

#### Google OAuth Login
- Google Sign-in is available as an alternative login option  
- Google authentication is handled using Streamlit OAuth  
- Only users already registered in the database are allowed to log in using Google  

---

## 💾 SQLite Database
### Database Setup
- Local SQLite database named `users.db`  
- Tables are created automatically on first run  

### Database Operations
- Create new users  
- Retrieve users during login  
- Update user passwords during password reset  

### Data Protection
- Only hashed passwords are stored  
- No sensitive data is saved in plain text  

---

## 🤖 GenAI Features

### Text Summarizer
#### Implementation
- Accepts short or long text input  
- Generates a 2–4 sentence summary  
- Uses OpenAI model `gpt-4o-mini`  
- Implemented via the OpenAI Responses API  

### Programming Tutor Chatbot
#### Implementation
- Integrated directly into the Streamlit interface  
- Designed as a task-focused programming tutor  
- Helps users understand:
  - Basic Python concepts  
  - SQLite and database queries  
  - This Streamlit project structure  
- Uses a non-trivial system prompt  
- Stores messages in `st.session_state["chat_history"]`  

---

## 🖥️ Streamlit User Interface
### Layout
- Clean and simple interface built with Streamlit  
- Uses tabs to separate features  

### Navigation
- Available tabs:
  - Summarizer  
  - Chatbot  

### UI Components
- Streamlit forms  
- Buttons and text inputs  
- Session state management  

---

## 📁 Project Structure
### Project Root

project-root/

│

├── app.py                # Main Streamlit application

├── auth_ui.py            # Authentication logic and UI

├── db.py                 # SQLite database functions

├── llm_utils.py          # AI summarizer and tutor chatbot logic

├── users.db              # SQLite database

├── requirements.txt      # Python dependencies

├── README.md             # Project documentation

│

└── .streamlit/

    └── secrets.toml      # API keys and OAuth configuration

---

## 🖥️ How to Run

1. **Install dependencies**

&emsp;&emsp; Make sure you have Python 3.10+ installed, then install the required packages:

   ```bash
   pip install streamlit
   pip install openai
   ```

2. **Set up your API key**

&emsp;&emsp; Create a file called my_secrets.py in the project root with the following content:

&emsp;&emsp;&emsp; OPENAI_API_KEY = "PASTE-YOUR-KEY-HERE"

3. **Run the app in the terminal**

&emsp;&emsp; streamlit run app.py

---

## 🌐 Deployment
### Public Access
- Deployed using Streamlit Community Cloud  
- Accessible through a public URL
- https://programming-project-iez4igqgdj7bqcmgzuxnww.streamlit.app/


---

## 🎓 Learning Outcomes
### Skills Gained
- Secure authentication implementation  
- Password hashing with bcrypt  
- Database management using SQLite  
- Google OAuth integration  
- Session handling with Streamlit  
- Task-focused Generative AI integration  
- Deployment of Python web applications  
