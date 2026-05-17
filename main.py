import json
import trello
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")
api_key = os.getenv("API_KEY")
workspaces_json = os.getenv("WORKSPACES", "[]")

workspace_options = json.loads(workspaces_json)
if not workspace_options:
    raise Exception("No workspaces defined in .env WORKSPACES variable")

print("Available workspaces:\n")
for i, name in enumerate(workspace_options, 1):
    print(f"  {i}. {name}")

while True:
    try:
        choice = int(input(f"\nSelect workspace (1-{len(workspace_options)}): "))
        if 1 <= choice <= len(workspace_options):
            break
        print(f"Please enter a number between 1 and {len(workspace_options)}")
    except ValueError:
        print("Please enter a valid number")

workspace_name = workspace_options[choice - 1]
print(f"\nSelected: {workspace_name}\n")

trello = trello.TrelloAPI(api_key, token)

old_workspaces = []
for workspace in trello.get_workspaces():
    print(workspace['displayName'] + '\n')
    if workspace['displayName'] == workspace_name:
        old_workspaces.append(workspace)
        
if len(old_workspaces) == 0:
    raise Exception(f"Workspace with name '{workspace_name}' not found")

old_workspace = old_workspaces[0]
old_workspace_id = old_workspace['id']

new_workspace = trello.create_workspace(workspace_name)

print(f"\nMoving boards from '{workspace_name}' to new workspace...")
all_boards = trello.get_workspace_boards(old_workspace_id)

for board in all_boards:
    board_name = board.get('name', 'Unknown')
    result = trello.move_board_to_workspace(board['id'], new_workspace['id'])
    print(f"  ✓ Moved board: {board_name}")

print(f"\nPromoting all board members to workspace admins...")
member_results = trello.add_all_board_members_to_workspace(new_workspace['id'], member_type='admin')
print(f"\n✓ Members promoted: {member_results['successful']}/{member_results['total']}")
if member_results['skipped'] > 0:
    print(f"⊘ Skipped: {member_results['skipped']} members (already workspace members)")
if member_results['failed'] > 0:
    print(f"✗ Failed to promote: {member_results['failed']} members")
print()

result = trello.delete_workspace(old_workspace_id)
if result:
    print(f"Workspace '{workspace_name}' deleted")
else:
    print(f"Failed to delete workspace '{workspace_name}'")