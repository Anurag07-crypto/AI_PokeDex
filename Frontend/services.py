from Work_dir.logger import get_logger
import os  
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from rembg import remove
from typing import Tuple
from PIL import Image 

logger = get_logger(__name__)


class BG_Remove:
    """BG_Remove for Removing Background Noise from the image for better output"""
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        
    def remove(self, bgcolor: Tuple[int, int, int, int] | None = None):
        """Remove Function to Access Remove method in rembg library"""
        
        image = Image.open(self.image_path).convert("RGBA")
        clear_image = remove(image, bgcolor=bgcolor)
        return clear_image
    
class LLM_Service:
    """LLM Service used to provide Groq LLM service with various models"""
    
    def __init__(self, context):
        self.context = context
        self.llm = None
        self.prompt = None
        self.response = None
    
    def invoke(self, model_name:str = "llama-3.1-8b-instant"):
        """Invoke Method to use the give and get info from GROQ_LLM""" 
        
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        if not GROQ_API_KEY:
            logger.critical("Missing API key")
            
        self.llm = ChatGroq(model=model_name)
        
        self.prompt = f""" 
    You have just only Write this things in more representative form
    in Markdown format
    here is the context:
    {self.context}
    constraints
    -make sure give me only one str output 
    -No extra messages only just do what i told above
    """
    
        self.response = self.llm.invoke(self.prompt)
        
        return self.response
    