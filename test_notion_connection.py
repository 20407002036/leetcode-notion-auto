
import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get Notion token from environment variable
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN environment variable not set. Please create a .env file.")

# Replace with your actual database ID (from Phase 1, Step 4)
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
if not NOTION_DATABASE_ID:
    raise ValueError("NOTION_DATABASE_ID environment variable not set. Please create a .env file.")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

# --- Test Function ---
def test_notion_connection():
    try:
        # Attempt to retrieve the database to verify the connection and ID
        objs = notion.databases.retrieve(database_id=NOTION_DATABASE_ID)
        print("Successfully connected to Notion and retrieved the database.")
        print(objs)
        return True
    except Exception as e:
        print(f"Error connecting to Notion: {e}")
        return False

if __name__ == "__main__":
    test_notion_connection()
