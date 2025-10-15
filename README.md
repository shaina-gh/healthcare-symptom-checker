# Healthcare Symptom Checker
A full-stack application that leverages a Large Language Model (LLM) to analyze user-provided symptoms and suggest potential conditions and next steps for educational purposes.

This project was built as a technical assignment to demonstrate proficiency in backend development, frontend integration, LLM prompting, and responsible AI safety practices.

## Demo Video


## 🌟 Key Features
### AI-Powered Analysis: 
Utilizes a powerful LLM (Anthropic's Claude) to provide nuanced suggestions based on symptom descriptions.

### Safety-First UI: 
The user interface requires users to acknowledge an educational disclaimer before they can input symptoms, demonstrating responsible design.

### Structured & Reliable Responses: 
Employs advanced prompt engineering to force the LLM to return responses in a clean JSON format, making the application robust and preventing errors.

### Dynamic Urgency Levels: 
The AI categorizes recommendations into 'Self-Care', 'Consult a Doctor', or 'Seek Immediate Medical Attention' based on the implied severity of the symptoms.

### Full-Stack Architecture: 
A modern stack featuring a Python/FastAPI backend and a React (Vite) frontend.

### Query History: 
Saves all previous checks in a local SQLite database, accessible through a "History" tab in the UI.

## 🛠️ Tech Stack
Backend: Python, FastAPI; 
Frontend: React (Vite); 
Database: SQLite; 
LLM Integration: Anthropic (Claude API)
