from pathlib import Path
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from .logger import get_logger
import os
from typing import Optional, List
from dotenv import load_dotenv 

logger = get_logger(__name__)

env_path = Path(__file__).resolve().parent.parent / ".env"

class Structure(BaseModel):
    Pokemon_name: str
    Evolve: Optional[List[str]] = None
    Attacks: List[str]
    Strongest_attack: List[str]
    Type: List[str]
    

def Agent(output_label, model:str="llama-3.3-70b-versatile"):
    """
    Agent for the user Support
    
    Args:
        output_label (_type_): String

    Raises:
        RuntimeError: Output Label Not Found

    Returns:
        _type_: Markdown string
    """
    
    load_dotenv(dotenv_path=env_path)

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    if not GROQ_API_KEY and TAVILY_API_KEY:
        logger.critical("Missing API keys")
        raise RuntimeError("Missing API keys")

    llm = ChatGroq(model=model, groq_api_key=GROQ_API_KEY)
    str_llm = llm.with_structured_output(Structure)
    
    try:
        tavily_search = TavilySearch(max_results=3, tavily_api_key=TAVILY_API_KEY)
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

