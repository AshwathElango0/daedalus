# Daedalus: Agentic Data Architect

Daedalus is an agentic, LLM-powered platform that turns natural language business requirements into actionable database schemas and ETL pipelines. It features user authentication, an admin panel, and a modern Gradio UI for interactive workflow.

## Features

- **User Authentication:** Register, log in, and manage sessions securely.
- **Admin Panel:** Admin user (admin/admin) can delete all users from the database.
- **Agentic LLM Workflow:**
  - Accepts business/data requirements in natural language.
  - Detects intent (schema, ETL, etc.), decomposes requirements, and plans reasoning steps.
  - Calls Gemini LLM for code generation and uses internal tools for validation.
  - Displays agent's reasoning steps and results in a clear, organized UI.
- **Modern UI:** Tabbed Gradio interface for authentication, agent interaction, and admin actions.
- **Security:** Passwords are hashed, and all actions are authorized and validated.

## Workflow Overview

1. **User registers or logs in.**
2. **User submits a business/data prompt.**
3. **Agent detects intent, decomposes the problem, and generates a solution (e.g., SQL schema, ETL code).**
4. **Agent validates and presents results, showing its reasoning steps.**
5. **Admin (if logged in) can delete all users from the admin panel.**
6. **If a user is deleted, they are automatically logged out on their next action.**

## Setup Instructions

1. **Clone the repository and navigate to the project directory.**

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root with your Gemini API key:
     ```env
     GOOGLE_API_KEY=your_google_gemini_api_key
     ```

5. **Run the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Run the Gradio UI:**
   ```bash
   python app/ui.py
   ```

7. **Access the UI:**
   - Open the Gradio link in your browser (usually http://localhost:7860)

## Default Admin User
- **Email:** admin
- **Password:** admin


