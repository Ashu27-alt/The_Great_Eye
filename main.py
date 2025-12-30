from ssd_check import check_func
from final_paths import gen_paths
from manager import manager_func
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import constants
import json
import torch
import logging
import pathlib

if check_func():
    with open(constants.CONFIG_PATH) as f:
        config = json.load(f)

    main_paths = config.get("watched_dir")

    if not isinstance(main_paths, list):
        raise ValueError("watched_dir must be a list of paths")

    final_paths = gen_paths(main_path=main_paths)
    
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b",dtype=torch.float16).to("mps")

    for path in final_paths:
        manager_func(path,processor,model)

else:
    print("SSD Disconnected")
