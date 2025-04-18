# app/utils/config_loader.py

"""It also includes a function to load phrases from a YAML file.
"""

from pathlib import Path

import toml
import yaml

CONFIG_DIR = Path("C:/Users/Abhi/Desktop/mlops/mlops4/customer_service_assistant/configs")


def load_toml_config(filename: str) -> dict:
    """Load a TOML configuration file."""
    config_path = CONFIG_DIR / filename
    with config_path.open() as f:
        return toml.load(f)


def load_yaml_config(filename: str) -> dict:
    """Load a YAML configuration file."""
    config_path = CONFIG_DIR / filename
    with config_path.open() as f:
        return yaml.safe_load(f)


def load_phrases() -> dict:
    """Load a YAML file containing phrases."""
    phrases_path = CONFIG_DIR / "phrases.yaml"
    with phrases_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)
