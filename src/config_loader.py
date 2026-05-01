import json
import os

def load_config(config_path="config.json"):
    """Loads the configuration from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON configuration: {e}")

if __name__ == "__main__":
    # Basic test of the config loader
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        print(json.dumps(config, indent=2))
    except Exception as e:
        print(f"Failed to load config: {e}")
