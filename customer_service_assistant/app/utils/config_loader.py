# app/utils/config_loader.py

from pathlib import Path

import toml
import yaml

CONFIG_DIR = Path("C:/Users/Abhi/Desktop/mlops/mlops4/customer_service_assistant/configs")


def load_toml_config(filename: str) -> dict:
    """Load a TOML configuration file."""
    config_path = CONFIG_DIR / filename
    with open(config_path) as f:
        return toml.load(f)


def load_yaml_config(filename: str) -> dict:
    """Load a YAML configuration file."""
    config_path = CONFIG_DIR / filename
    with open(config_path) as f:
        return yaml.safe_load(f)

def load_phrases() -> dict:
    """Load a YAML file containing phrases."""
    phrases_path = CONFIG_DIR / "phrases.yaml"
    with open(phrases_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
