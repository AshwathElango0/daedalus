import gradio as gr
import requests
import re

API_URL = "http://localhost:8000"

global_state = {"token": None, "user": None}

FORCED_LOGOUT_MSG = "You have been logged out because your account was deleted. Please register or log in again."

def strip_code_block(text):
    if text is None:
        return ""
    return re.sub(r"^```[a-zA-Z]*\\n|```$", "", text.strip(), flags=re.MULTILINE)

def register_user(email, password):
    resp = requests.post(f"{API_URL}/users/register", json={"email": email, "password": password})
    if resp.ok:
        return "Registration successful! Please log in.", False
    try:
        detail = resp.json().get('detail', 'Unknown error')
    except Exception:
        detail = resp.text or 'Unknown error'
    return f"Registration failed: {detail}", True

def login_user(email, password):
    resp = requests.post(f"{API_URL}/users/login", json={"email": email, "password": password})
    if resp.ok:
        data = resp.json()
        global_state["token"] = data["token"]
        global_state["user"] = data["user"]
        return f"Welcome, {data['user']['email']}!", False
    try:
        detail = resp.json().get('detail', 'Invalid credentials')
    except Exception:
        detail = resp.text or 'Invalid credentials'
    return f"Login failed: {detail}", True

def logout_user(forced=False):
    global_state["token"] = None
    global_state["user"] = None
    msg = FORCED_LOGOUT_MSG if forced else "Logged out."
    return gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), msg

def query_agent(prompt):
    if not global_state["token"]:
        return "Please log in first.", "", ""
    headers = {"token": global_state["token"]}
    resp = requests.post(f"{API_URL}/agent/process", json={"prompt": prompt}, headers=headers)
    if resp.status_code == 401:
        # Forced logout
        logout_user(forced=True)
        return FORCED_LOGOUT_MSG, "", ""
    if not resp.ok:
        return "Error from agent.", "", ""
    data = resp.json()
    steps_md = "\n".join([f"**Step {i+1}:** {step}" for i, step in enumerate(data.get("steps", []))])
    result = data.get("result", {})
    if data.get("intent") == "schema":
        schema_sql = strip_code_block(result.get('schema_sql', ''))
        result_md = f"### Entities\n{result.get('entities', [])}\n\n### Generated SQL Schema\n```sql\n{schema_sql}\n```\n\n### Validation\n{result.get('validation', {})}"
        llm_response = schema_sql
    elif data.get("intent") == "etl":
        etl_code = strip_code_block(result.get('etl_code', ''))
        result_md = f"### Generated ETL Code\n```python\n{etl_code}\n```"
        llm_response = etl_code
    else:
        response = strip_code_block(result.get('response', ''))
        result_md = response
        llm_response = response
    return steps_md, result_md, llm_response

def delete_all_users():
    if not global_state["token"] or not global_state["user"] or global_state["user"]["email"] != "admin":
        return "Not authorized. Only admin can perform this action."
    headers = {"token": global_state["token"]}
    resp = requests.delete(f"{API_URL}/users/admin/delete_all_users", headers=headers)
    if resp.ok:
        return resp.json().get("message", "All users deleted.")
    try:
        detail = resp.json().get('detail', 'Unknown error')
    except Exception:
        detail = resp.text or 'Unknown error'
    return f"Failed to delete users: {detail}"

with gr.Blocks() as demo:
    gr.Markdown("# Daedalus Agent Test UI")
    login_state = gr.State()
    with gr.Tab("Authentication"):
        with gr.Row():
            with gr.Column():
                email = gr.Textbox(label="Email")
                password = gr.Textbox(label="Password", type="password")
                login_btn = gr.Button("Login")
                register_btn = gr.Button("Register")
                auth_msg = gr.Markdown(visible=False)
            with gr.Column():
                logout_btn = gr.Button("Logout", visible=False)
    with gr.Tab("Agent"):
        with gr.Row():
            prompt = gr.Textbox(label="Business Requirement / Prompt", lines=4)
            submit_btn = gr.Button("Submit", visible=False)
        steps_out = gr.Markdown(label="Agent Reasoning Steps")
        result_out = gr.Markdown(label="Agent Result")
        llm_out = gr.Textbox(label="LLM Raw Output", lines=8, interactive=False)
    with gr.Tab("Admin Panel"):
        admin_msg = gr.Markdown("", visible=False)
        delete_btn = gr.Button("Delete All Users", visible=False)

    def show_agent_area():
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

    def show_admin_panel():
        is_admin = global_state["user"] and global_state["user"]["email"] == "admin"
        return gr.update(visible=is_admin), gr.update(visible=is_admin)

    login_btn.click(lambda e, p: login_user(e, p), [email, password], [auth_msg, login_btn],
                   queue=False).then(lambda: show_agent_area(), None, [login_btn, register_btn, submit_btn])
    register_btn.click(lambda e, p: register_user(e, p), [email, password], [auth_msg, register_btn], queue=False)
    logout_btn.click(logout_user, None, [login_btn, register_btn, logout_btn, auth_msg], queue=False)
    submit_btn.click(query_agent, [prompt], [steps_out, result_out, llm_out], queue=False)
    delete_btn.click(delete_all_users, None, admin_msg, queue=False)

    demo.load(show_admin_panel, None, [admin_msg, delete_btn])

    if global_state["token"]:
        login_btn.visible = False
        register_btn.visible = False
        submit_btn.visible = True
        logout_btn.visible = True
        delete_btn.visible = global_state["user"]["email"] == "admin"
        admin_msg.visible = global_state["user"]["email"] == "admin"

if __name__ == "__main__":
    demo.launch() 