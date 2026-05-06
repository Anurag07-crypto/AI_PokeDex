from pathlib import Path
import sys


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from Work_dir.logger import get_logger
from Work_dir.pokedex_agent import Agent

logger = get_logger(__name__)

app = FastAPI(title="Pokedex")

class Dex_str(BaseModel):
    query:str

@app.post("/get_info")
def get_info(request:Dex_str):
    """ Getting info from the frontend and passes request """
    
    logger.info(f"Incoming Request {request.query[:50]}")
    try:
        response = Agent(output_label=request.query)
        logger.info("Backend Request Approved")
        return {"response":response}
    
    except RuntimeError as e:
        logger.error(f"Runtime Error in /get_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected Error in /get_info: {e}", exc_info=True) 
        raise HTTPException(
            status_code=500,
            detail="Something went Wrong Try Again"
        )
        
if __name__ == "__main__":
    
    uvicorn.run("back_server:app", port=8000, host="127.0.0.1", reload=True)
