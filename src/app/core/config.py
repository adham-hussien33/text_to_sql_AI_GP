import yaml

CONFIG_PATH = "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

MODEL_PATH = config["MODEL_PATH"]
CHROMA_PATH = config["CHROMA_PATH"]
CONFIDENCE_THRESHOLD = config["CONFIDENCE_THRESHOLD"]


