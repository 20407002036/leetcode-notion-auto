import os
import datetime
from notion_client import Client
from dotenv import load_dotenv
import json

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


def get_existing_leets():
    """
    Get the existing Leets in the db
    :return:
    """
    res = notion.databases.query(
        database_id=NOTION_DATABASE_ID,
      )

    for obj in res["results"]:
        print(obj["id"])
        print(f" {obj["properties"]["Name"]["title"][0]["text"]["content"]}")
        print(f" {obj["properties"]["Number"]["number"]}")
        print(f" {obj["properties"]["Difficulty Level"]["select"]["name"]}")
        print(f" {obj["properties"]["Reviewed"]["status"]}")

    # print(json.dumps(res["results"], indent=2))
    return res
def add_leetcode_entry(problem_name, leetNumber, difficulty, solution_link, date_solved=None, status="Not Yet"):
    """
    Adds a new entry to your Notion LeetCode database.

    Args:
        problem_name (str): The name of the LeetCode problem.
        difficulty (str): The difficulty (e.g., "Easy", "Medium", "Hard").
                          Must match options in your Notion Difficulty select property.
        solution_link (str): URL to your solution (e.g., GitHub Gist, personal repo).
        date_solved (str, optional): Date solved in YYYY-MM-DD format. Defaults to today.
        status (str, optional): The status (e.g., "Solved").
                                Must match options in your Notion Status select property.
    """
    if not date_solved:
        date_solved = datetime.date.today().isoformat()  # YYYY-MM-DD format

    try:
        response = notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Name": {  # This must exactly match your Notion database's Title property name
                    "title": [
                        {
                            "text": {
                                "content": problem_name
                            }
                        }
                    ]
                },
                "Number":{
                    "number": int(leetNumber),
                },
                "Difficulty Level": {  # This must exactly match your Notion database's Select property name
                    "select": {
                        "name": difficulty
                    }
                },
                # "Solution Link": {  # This must exactly match your Notion database's URL property name
                #     "url": solution_link
                # },
                "Date": {  # This must exactly match your Notion database's Date property name
                    "date": {
                        "start": date_solved
                    }
                },
                "Status": {  # This must exactly match your Notion database's Select property name
                    "select": {
                        "name": status
                    }
                }
            }
        )
        print(f"Successfully added '{problem_name}' to Notion!")
        # Optional: Print the URL to the new page
        # print(f"Notion Page URL: {response['url']}")

    except Exception as e:
        print(f"Error adding entry to Notion: {e}")
        print("Please check: ")
        print("- Your Notion token is correct and has access to the database.")
        print("- Your database ID is correct.")
        print(
            "- Property names (Name, Difficulty, Solution Link, Date Solved, Status) exactly match those in Notion (case-sensitive).")
        print("- Select options (Easy, Medium, Hard, Solved) exactly match those in Notion (case-sensitive).")


if __name__ == "__main__":
    print("--- Add New LeetCode Entry to Notion ---")
    # problem_name = input("Enter LeetCode Problem Name: ")
    # leetNumber = input("Enter LeetCode Problem Number: ")

    problem_name = "Name"
    leetNumber= 6481

    difficulty = "Easy"
    solution_link = "GitHub Gist"

    # Input validation for difficulty
    # valid_difficulties = ["Easy", "Medium", "Hard"]
    # difficulty = ""
    # while difficulty not in valid_difficulties:
    #     difficulty = input(f"Enter Difficulty ({'/'.join(valid_difficulties)}): ").strip().title()
    #     if difficulty not in valid_difficulties:
    #         print(f"Invalid difficulty. Please choose from {', '.join(valid_difficulties)}.")
    #
    # solution_link = input("Enter Link to your Solution (e.g., GitHub URL): ")

    # You can extend this to ask for other properties if you add them
    # For now, Date Solved defaults to today and Status to "Solved"

    get_existing_leets()
    # add_leetcode_entry(problem_name, leetNumber, difficulty, solution_link)
