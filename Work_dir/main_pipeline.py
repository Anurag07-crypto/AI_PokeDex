from Work_dir.Cnn_model import Predict
from Work_dir.pokedex_agent import Agent
from .logger import get_logger

logger = get_logger(__name__)

def WorkFlow(img_path):
    """Mainly the important workflow pipeline

    Args:
        img_path (_type_): Path of image

    Raises:
        RuntimeError: Image Path Not Loaded

    Returns:
        _type_: String and Integer
    """
    try:
        label, confidence_score = Predict(img_path=img_path)
        response = Agent(label)
        logger.info("Label, Confidence Score and Final Response Generated")
        return label, confidence_score, response

    except Exception as e:
        logger.critical(f"Image Path not Loaded: {e}")
        raise RuntimeError(f"Image Path not Loaded: {e}") from e 
