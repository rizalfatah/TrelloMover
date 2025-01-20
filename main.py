import json
import trello
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

token = os.getenv("TOKEN")
api_key = os.getenv("API_KEY")

old_workspace_name = os.getenv("OLD_WORKSPACE_NAME")
new_workspace_name = os.getenv("NEW_WORKSPACE_NAME")

trello = trello.TrelloAPI(api_key, token)

workspaces = trello.get_workspaces()

old_workspaces = []
for workspace in trello.get_workspaces():
    print(workspace['displayName'] + '\n')
    if (workspace['displayName'] == old_workspace_name):
        old_workspaces.append(workspace)
        
if (len(old_workspaces) == 0):
    raise Exception(f"Workspace with name '{old_workspace_name}' not found")

# get only the first workspace if there are more than one workspaces with the same name
old_workspace = old_workspaces[0]
old_workspace_id = old_workspace['id']

# create workspace with original name
new_workspace = trello.create_workspace(new_workspace_name)

# move board old workspace into new workspace
all_boards = trello.get_workspace_boards(old_workspace_id)
print(all_boards)
for board in all_boards:
    result = trello.move_board_to_workspace(board['id'], new_workspace['id'])
    print(f"Pindah board: {result}")

# delete old workspace
result = trello.delete_workspace(old_workspace_id)
if (result):
    print(f"Workspace '{old_workspace_name}' deleted")
else:
    print(f"Failed to delete workspace '{old_workspace_name}'")