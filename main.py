import os
import datetime
from notion_client import Client
from dotenv import load_dotenv
import json
from utils.fileUtils import extract_file_text
from pathlib import Path
from Models.SavedLeetMdl import getNotionLeetsFromdb

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get Notion token from environment variable
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PATH_TO_LEETCODE_FOLDER = os.getenv("PATH_TO_LEETCODE_FOLDER")

if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN environment variable not set. Please create a .env file.")

# Replace with your actual database ID (from Phase 1, Step 4)
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
if not NOTION_DATABASE_ID:
    raise ValueError("NOTION_DATABASE_ID environment variable not set. Please create a .env file.")


from Leet.main import Leet
leet = Leet(NOTION_TOKEN)

def newImp(problem_name, leetNumber, difficulty, solution_link):
    leet.add_leetcode_entry(NOTION_DATABASE_ID, problem_name, leetNumber, difficulty, datetime.date.today().isoformat(), status="Not Yet")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)


def get_files_under_leet_folder(LeetCodeFolder):
    path = Path(LeetCodeFolder)
    file_names = []
    for x, y, z in path.walk():
        for file_name in z:
            file_names.append(file_name)
    # print(file_names)
    return file_names

def get_existing_leets():
   res = leet.get_saved_leets(NOTION_DATABASE_ID) # Notion Entries
   dbNotionLeets = getNotionLeetsFromdb() #  Local db entries
   exiting_leet_No = [dbleet[1] for dbleet in dbNotionLeets if len(dbNotionLeets)>=0] # Hardcoded position of the leet_no
   for entry in res:
       # print(entry.leetNo)
       if entry.leetNo not in tuple(exiting_leet_No):
           if entry.leetNo is None:
               print(f"LeetCode entry {entry.leetName} Has no Leetcode Number associated to it.")
               continue
           entry.saveNotionLeet()

if __name__ == "__main__":
    print("--- Add New LeetCode Entry to Notion ---")

    get_existing_leets()

    file_Names = get_files_under_leet_folder(PATH_TO_LEETCODE_FOLDER)
    savedLeetIds = []
    for file_Name in file_Names:
        has = False
        if "~" in file_Name: # Eliminated Emacs auto saved buffers
            has = True
        if not has:
            leetId = extract_file_text(f"{PATH_TO_LEETCODE_FOLDER}/{file_Name}")
            savedLeetIds.append(leetId)

    # newImp(problem_name, leetNumber, difficulty, solution_link)
