from ssd_check import check_func
from final_paths import gen_paths
from manager import manager_func
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import constants
import json
import torch
import logging.config
import pathlib

def extra():
    logger = logging.getLogger("The_Great_Eye")  # __name__ is a common choice


    def setup_logging():
        config_file = pathlib.Path("/Users/ashutosh/The_Great_Eye/logging.config.json")
        with open(config_file) as f_in:
            config = json.load(f_in)

            logging.config.dictConfig(config)

    setup_logging()
    logger = logging.getLogger("my_app")

    if not check_func():
        logger.error("SSD Disconnected")
        exit(1)

    with open(constants.CONFIG_PATH) as f:
        config = json.load(f)

    main_paths = config.get("watched_dir")
    if not isinstance(main_paths, list):
        raise ValueError("watched_dir must be a list")

    paths = gen_paths(main_path=main_paths)

    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b",dtype=torch.float16).to("mps")

    with torch.no_grad():
        for path in paths:
            if not check_func():
                logger.warning("SSD disconnected mid-run")
                break
            manager_func(path, processor, model, logger)
            logger.info(f"done with {path}")
