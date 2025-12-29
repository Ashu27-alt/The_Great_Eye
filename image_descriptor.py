from PIL import Image
import torch
from pillow_heif import register_heif_opener

register_heif_opener()

DEVICE = "mps"

def describe(image_path,processor,model):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        image,
        return_tensors="pt"
    ).to(DEVICE, torch.float16)

    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=50)

    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )
    return caption.strip()

