from notion_client import Client

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