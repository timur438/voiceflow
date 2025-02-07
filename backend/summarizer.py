from llama_cpp import Llama
import os
import requests
from tqdm import tqdm

class TranscriptSummarizer:
    def __init__(self, model_name="mistral-7b-instruct-v0.2.Q4_K_M.gguf"):
        """Initialize the summarizer with auto-downloading model capability"""
        self.models_dir = "models"
        self.model_path = os.path.join(self.models_dir, model_name)
        self.model_url = f"https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/{model_name}"
        
        os.makedirs(self.models_dir, exist_ok=True)
        
        if not os.path.exists(self.model_path):
            self._download_model()
            
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=8192,
            n_gpu_layers=-1
        )

    def _download_model(self):
        """Download the model from HuggingFace"""
        print(f"Downloading model to {self.model_path}...")
        response = requests.get(self.model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(self.model_path, 'wb') as file, tqdm(
            desc=self.model_path,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
