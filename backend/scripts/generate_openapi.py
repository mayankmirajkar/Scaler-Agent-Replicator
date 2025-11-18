# backend/scripts/generate_openapi.py
import json
import yaml
from app.main import app

def main():
    openapi = app.openapi()
    with open("openapi.json", "w") as f:
        json.dump(openapi, f, indent=2)
    with open("api.yml", "w") as f:
        yaml.dump(openapi, f, sort_keys=False)

if __name__ == "__main__":
    main()
