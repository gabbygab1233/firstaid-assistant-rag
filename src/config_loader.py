import os
import yaml

def load_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, "config.yaml")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Resolving paths to be absolute paths
    for key, value in config.get('paths', {}).items():
        if isinstance(value, list):
            # If it's a list, process each path in the list
            config['paths'][key] = [os.path.join(base_dir, path) for path in value]
        else:
            # If it's a single string, resolve the path
            config['paths'][key] = os.path.join(base_dir, value)
    
    return config