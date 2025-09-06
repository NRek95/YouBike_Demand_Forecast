# constants.py
from pathlib import Path

# This dynamically finds the root directory of your project
PROJECT_ROOT = Path(__file__).resolve().parent

# This builds a path to the 'data' folder from the project root
# Your code will use this variable to find the data
DATA_DIR = PROJECT_ROOT / "data"

# Example of a full path to a specific file
# DATA_FILE_PATH = DATA_DIR / "your_large_dataset.parquet"
