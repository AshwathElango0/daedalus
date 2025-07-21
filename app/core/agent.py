import re
from typing import Dict, Any
from app.core.llm import generate_gemini_response
from app.core.tools import validate_sql_schema
from app.utils.llm import strip_code_block

# --- Intent Detection ---
def detect_intent(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ["schema", "table", "entity", "database"]):
        return "schema"
    if any(word in prompt_lower for word in ["etl", "pipeline", "extract", "transform", "load"]):
        return "etl"
    return "unknown"

# --- Decomposition (for schema) ---
def extract_entities(prompt: str) -> list:
    # Simple regex-based entity extraction (improve with LLM later)
    entities = re.findall(r"([A-Z][a-zA-Z0-9_]+)", prompt)
    return list(set(entities))

# --- Orchestrator ---
async def agent_orchestrator(prompt: str) -> Dict[str, Any]:
    intent = detect_intent(prompt)
    steps = []
    result = {}

    if intent == "schema":
        steps.append("Extract entities from prompt")
        entities = extract_entities(prompt)
        result["entities"] = entities

        steps.append("Ask LLM to generate SQL schema for entities")
        llm_schema_prompt = f"Generate a normalized SQL schema for the following entities: {entities}. Include primary and foreign keys. Output only SQL DDL statements."
        schema_sql = await generate_gemini_response(llm_schema_prompt)
        schema_sql_clean = strip_code_block(schema_sql)
        result["schema_sql"] = schema_sql_clean

        steps.append("Validate generated SQL schema")
        validation = validate_sql_schema(schema_sql_clean)
        result["validation"] = validation

    elif intent == "etl":
        steps.append("Ask LLM to generate ETL pipeline code for the described process")
        etl_code = await generate_gemini_response(f"Generate a Python ETL pipeline for: {prompt}")
        etl_code_clean = strip_code_block(etl_code)
        result["etl_code"] = etl_code_clean
    else:
        steps.append("Intent not recognized. Ask LLM for clarification or best effort.")
        fallback = await generate_gemini_response(f"{prompt}\nIf unclear, ask clarifying questions.")
        fallback_clean = strip_code_block(fallback)
        result["response"] = fallback_clean

    return {"intent": intent, "steps": steps, "result": result} 