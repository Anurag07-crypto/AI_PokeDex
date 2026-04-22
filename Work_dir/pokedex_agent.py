from pathlib import Path
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from .logger import get_logger
import os
from typing import Optional, List
from dotenv import load_dotenv 

'''
led', 'failed_generation': '<function=Structure> {"Attacks": ["Scratch", "Night Slash", "Feint Attack", "Power Gem", "Foul Play"], "Evolutions": null, "Pokemon_name": "Persian", "Strongest_attack": "Scratch and Foul Play", "Type": ["Normal"]}'}}
2026-04-21 14:14:57 | ERROR    | back_server | Runtime Error in /get_info: Output Label Not Found: Error code: 400 - {'error': {'message': "Failed to call a function. Please adjust your prompt. See 'failed_generation' for more details.", 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '<function=Structure> {"Attacks": ["Scratch", "Night Slash", "Feint Attack", "Power Gem", "Foul Play"], "Evolutions": null, "Pokemon_name": "Persian", "Strongest_attack": "Scratch and Foul Play", "Type": ["Normal"]}'}}
'''



logger = get_logger(__name__)

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not groq_api_key:
    logger.critical("Missing GROQ_API_KEY")
    raise RuntimeError("Missing GROQ_API_KEY")

if not tavily_api_key:
    logger.critical("Missing TAVILY_API_KEY")
    raise RuntimeError("Missing TAVILY_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

class Structure(BaseModel):
    Pokemon_name: str
    Evolve: Optional[List[str]] = None
    Attacks: List[str]
    Strongest_attack: List[str]
    Type: List[str]
str_llm = llm.with_structured_output(Structure)

def Agent(output_label):
    try:
        tavily_search = TavilySearch(max_results=3, tavily_api_key=tavily_api_key)
        query = f"{output_label} Pokemon, evolve, type, attacks and strongest move"
        search_results = tavily_search.invoke({"query":query})
        logger.info("Search Results generated")
        PROMPT = f"""
    You are a Pokemon expert.

    Use ONLY the provided context to extract information about the Pokemon.

    Context:
    {search_results}

    Instructions:
    - Extract accurate information
    - Do NOT hallucinate
    - If a field is missing, return null

    Return data that fits the required schema.
    """

        response = str_llm.invoke([HumanMessage(content=PROMPT)])
        logger.info("Response Generated")
        return response
    except Exception as e:
        logger.error(f"Output label Not Found: {e}")
        raise RuntimeError(f"Output Label Not Found: {e}") from e

