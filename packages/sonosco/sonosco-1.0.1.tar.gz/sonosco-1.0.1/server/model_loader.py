import os
import logging

from sonosco.inference.deepspeech2_inference import DeepSpeech2Inference
from sonosco.inference.las_inference import LasInference


model_id_to_inference = {
    "deepspeech2": DeepSpeech2Inference,
    "las1": LasInference,
    "las4": LasInference,
    "las5": LasInference
}


# TODO: lazy loading
def load_models(config):
    models = dict()

    for model_config in config:
        if model_config.get('external'):
            pass
        else:
            try:
                model_path = model_config["path"]
                if not os.path.exists(model_path):
                    logging.warning(f"Model {model_config['id']} does not exist in {model_path}. Skipping..")
                    continue
                models[model_config["id"]] = model_id_to_inference[model_config["id"]](model_config["path"])
            except Exception as e:
                logging.error(f"Could not load {model_config['id']}, because of {e}")

    return models
