from typing import Any
from notion_client import Client
from Models.SavedLeetMdl import SavedLeetMdl

class Leet:
    def __init__(self, notion_token):
        self.notion_token = notion_token
        self.notion = self.__initialize_notion_instance()

    def __initialize_notion_instance(self):
        return Client(auth=self.notion_token)

    def add_leetcode_entry(self, notion_db_id, problem_name, leet_number, difficulty, date_solved, status):
        try:
            response = self.notion.pages.create(
                parent={"database_id": notion_db_id},
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
                    "Number": {
                        "number": int(leet_number),
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
            print(f"{response}\n")
        except Exception as e:
            print(f"Error adding entry to Notion: {e}")

    def get_saved_leets(self, notion_db_id) -> list[Any] | None:
        leetLst = []
        try:
            response = self.notion.databases.query(
                database_id = notion_db_id
            )
            for obj in response["results"]:
                leet_notion_id = obj["id"]
                leet_title = obj["properties"]["Name"]["title"][0]["text"]["content"]
                leet_no = obj["properties"]["Number"]["number"]
                leet_difficulty = obj["properties"]["Difficulty Level"]["select"]["name"]
                leet_status = obj["properties"]["Reviewed"]["status"]

                print(leet_notion_id)
                print(f"  {leet_title}")
                print(f"  {leet_difficulty}")
                print(f"  {leet_status}")
                print(f"  {leet_no}")
                notionLeet = SavedLeetMdl(leet_no, leet_title, leet_notion_id, leet_difficulty, leet_status)
                leetLst.append(notionLeet)
            # print(type(leetLst))
            return leetLst

        except Exception as e:
            print(f"Error getting existing entries from Notion: {e}")
