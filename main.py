import os
import datetime
import logging
from notion_client import Client
from dotenv import load_dotenv
import json
from utils.fileUtils import extract_file_text
from utils.textParser import parse_leet_data_from_extracted_text
from pathlib import Path
# from Models.SavedLeetMdl import getNotionLeetsFromdb  # TODO: Fix import path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('leetcode_automator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get Notion token from environment variable
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PATH_TO_LEETCODE_FOLDER = os.getenv("PATH_TO_LEETCODE_FOLDER")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Validate environment variables
if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN environment variable not set. Please create a .env file.")

if not PATH_TO_LEETCODE_FOLDER:
    raise ValueError("PATH_TO_LEETCODE_FOLDER environment variable not set. Please create a .env file.")

if not NOTION_DATABASE_ID:
    raise ValueError("NOTION_DATABASE_ID environment variable not set. Please create a .env file.")

# Validate LeetCode folder
leetcode_path = Path(PATH_TO_LEETCODE_FOLDER)
if not leetcode_path.exists():
    raise FileNotFoundError(f"LeetCode folder not found: {PATH_TO_LEETCODE_FOLDER}")

if not leetcode_path.is_dir():
    raise NotADirectoryError(f"PATH_TO_LEETCODE_FOLDER is not a directory: {PATH_TO_LEETCODE_FOLDER}")

logger.info(f"Using LeetCode folder: {PATH_TO_LEETCODE_FOLDER}")


from Leet.main import Leet
leet = Leet(NOTION_TOKEN)

def add_leetcode_entry(problem_name, leet_number, difficulty, solution_link):
    """Add a new LeetCode entry to Notion"""
    leet.add_leetcode_entry(NOTION_DATABASE_ID, problem_name, leet_number, difficulty, datetime.date.today().isoformat(), status="Not Yet")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)


def get_files_under_leet_folder(leetcode_folder):
    """Get all Python files in the LeetCode folder"""
    path = Path(leetcode_folder)
    
    if not path.exists():
        raise FileNotFoundError(f"LeetCode folder not found: {leetcode_folder}")
    
    file_names = []
    # Use rglob for recursive search, filtering Python files and excluding temp files
    for file_path in path.rglob('*.py'):
        if file_path.is_file() and '~' not in file_path.name:
            file_names.append(file_path.name)
    
    return file_names

def get_existing_leets():
    """Sync Notion entries to local database"""
    try:
        res = leet.get_saved_leets(NOTION_DATABASE_ID) # Notion Entries
        # TODO: Fix import path for getNotionLeetsFromdb
        # dbNotionLeets = getNotionLeetsFromdb() #  Local db entries
        # For now, assume empty local DB until import is fixed
        dbNotionLeets = []
        exiting_leet_No = [dbleet[1] for dbleet in dbNotionLeets if len(dbNotionLeets) >= 0]
        
        synced_count = 0
        for entry in res:
            if entry.leetNo not in tuple(exiting_leet_No):
                if entry.leetNo is None:
                    logger.warning(f"LeetCode entry '{entry.leetName}' has no number associated")
                    continue
                entry.saveNotionLeet()
                synced_count += 1
                logger.info(f"Synced LeetCode #{entry.leetNo} to local database")
        
        logger.info(f"Synced {synced_count} new entries from Notion")
        
    except Exception as e:
        logger.error(f"Error syncing Notion entries: {e}")
        raise

if __name__ == "__main__":
    logger.info("=== LeetCode Notion Automator Started ===")

    # Sync existing entries
    logger.info("Syncing existing Notion entries...")
    get_existing_leets()

    # Process local files
    logger.info("Processing local LeetCode files...")
    file_names = get_files_under_leet_folder(PATH_TO_LEETCODE_FOLDER)
    logger.info(f"Found {len(file_names)} Python files to process")
    
    processed_files = []
    
    for file_name in file_names:
        try:
            file_path = f"{PATH_TO_LEETCODE_FOLDER}/{file_name}"
            file_text = extract_file_text(file_path)
            
            if not file_text:
                logger.warning(f"Could not read file {file_name}")
                continue
            
            leet_number = parse_leet_data_from_extracted_text(file_text)
            
            if leet_number:
                logger.info(f"✓ Found LeetCode #{leet_number} in {file_name}")
                processed_files.append({
                    'file': file_name,
                    'leet_number': leet_number
                })
                
                # TODO: Add logic to create Notion entry if not exists
                # add_leetcode_entry(problem_name, leet_number, difficulty, solution_link)
                
            else:
                logger.debug(f"No LeetCode data found in {file_name}")
                
        except Exception as e:
            logger.error(f"Error processing {file_name}: {e}")
    
    logger.info(f"Successfully processed {len(processed_files)} files")
    for pf in processed_files:
        logger.info(f"  - {pf['file']}: LeetCode #{pf['leet_number']}")
    logger.info("=== LeetCode Notion Automator Completed ===")

    # add_leetcode_entry(problem_name, leet_number, difficulty, solution_link)
