from PyQt5.QtCore import QThread, pyqtSignal
from core.Embedding.clip_embedder import Embedder
from transformers import CLIPModel,CLIPProcessor

class EmbedWorker(QThread):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    progress=pyqtSignal(int)

    def __init__(self, *, mode, payload, model, processor,device):
        super().__init__()
        self.mode = mode       
        self.payload = payload  
        self.model = model
        self.processor = processor
        self.device = device

    def emit_progress(self, percent):
        self.progress.emit(percent)
    
    def run(self):
        if self.model is None or self.processor is None:
            self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
            self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        if self.mode == "image":
            Embedder.image_embedder(
                path=self.payload,
                model=self.model,
                processor=self.processor,
                device=self.device,
                progressCallback=self.emit_progress
            )
            self.finished.emit()

        elif self.mode == "text":
            vector = Embedder.text_embedder(
                query=self.payload,
                model=self.model,
                processor=self.processor,
                device=self.device
            )
            self.result.emit(vector)
            self.finished.emit()
