import logging
from llama_cpp import Llama
from src.deploy.config import settings

# Setting up logging for the loader
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        """Loads the model into memory if not already loaded."""
        if self._model is None:
            logger.info(f"Loading model from {settings.MODEL_PATH}...")
            try:
                if settings.MODEL_TYPE == "gguf":
                    self._model = Llama(
                        model_path=settings.MODEL_PATH,
                        n_ctx=2048,  # Setting context window
                        n_threads=4, # Adjusting threads for CPU
                        n_gpu_layers=0 # Enabling GPU layers if available (e.g., 32 for T4)
                    )
                else:
                    raise ValueError(f"Unsupported model type: {settings.MODEL_TYPE}")
                
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise e
        return self._model

    def get_model(self):
        """Returns the loaded model instance."""
        if self._model is None:
            return self.load_model()
        return self._model

# Creating a singleton instance of the loader
model_loader = ModelLoader()
