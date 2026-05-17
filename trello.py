import requests
from typing import Dict, List, Optional, Any
import json

class TrelloAPI:
    """
    A class to interact with Trello API for workspace management
    """
    
    BASE_URL = "https://api.trello.com/1"
    
    def __init__(self, api_key: str, token: str):
        """
        Initialize TrelloAPI with authentication credentials
        
        Args:
            api_key (str): Your Trello API key
            token (str): Your Trello API token
        """
        self.api_key = api_key
        self.token = token
        self.auth_params = {
            'key': self.api_key,
            'token': self.token
        }
    
    def get_workspaces(self) -> List[Dict[str, Any]]:
        """
        Get all workspaces (organizations) for the authenticated user
        
        Returns:
            List[Dict[str, Any]]: List of workspaces
        """
        endpoint = f"{self.BASE_URL}/members/me/organizations"
        response = requests.get(endpoint, params=self.auth_params)
        response.raise_for_status()
        return response.json()
    
    def get_workspace_details(self, workspace_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific workspace
        
        Args:
            workspace_id (str): ID of the workspace
            
        Returns:
            Dict[str, Any]: Workspace details
        """
        endpoint = f"{self.BASE_URL}/organizations/{workspace_id}"
        response = requests.get(endpoint, params=self.auth_params)
        response.raise_for_status()
        return response.json()
    
    def create_workspace(
        self, 
        display_name: str, 
        name: Optional[str]= None, 
        desc: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new workspace
        
        Args:
            name (str): Name of the workspace (used in URLs)
            display_name (str): Display name of the workspace
            desc (Optional[str]): Description of the workspace
            
        Returns:
            Dict[str, Any]: Created workspace details
        """
        endpoint = f"{self.BASE_URL}/organizations"
        params = {
            **self.auth_params,
            'displayName': display_name,
            'name': name,
        }
        if desc:
            params['desc'] = desc
            
        response = requests.post(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def move_board_to_workspace(
        self, 
        board_id: str, 
        target_workspace_id: str
    ) -> Dict[str, Any]:
        """
        Move a board to a different workspace
        
        Args:
            board_id (str): ID of the board to move
            target_workspace_id (str): ID of the target workspace
            
        Returns:
            Dict[str, Any]: Updated board details
        """
        endpoint = f"{self.BASE_URL}/boards/{board_id}/idOrganization"
        params = {
            **self.auth_params,
            'value': target_workspace_id
        }
        response = requests.put(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def delete_workspace(self, workspace_id: str) -> bool:
        """
        Delete a workspace
        
        Args:
            workspace_id (str): ID of the workspace to delete
            
        Returns:
            bool: True if deletion was successful
        """
        endpoint = f"{self.BASE_URL}/organizations/{workspace_id}"
        response = requests.delete(endpoint, params=self.auth_params)
        response.raise_for_status()
        return response.status_code == 200
    
    def update_workspace(
        self, 
        workspace_id: str,
        name: Optional[str] = None,
        display_name: Optional[str] = None,
        desc: Optional[str] = None,
        website: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update workspace details
        
        Args:
            workspace_id (str): ID of the workspace to update
            name (Optional[str]): New name for the workspace
            display_name (Optional[str]): New display name
            desc (Optional[str]): New description
            website (Optional[str]): New website URL
            
        Returns:
            Dict[str, Any]: Updated workspace details
        """
        endpoint = f"{self.BASE_URL}/organizations/{workspace_id}"
        params = {**self.auth_params}
        
        if name:
            params['name'] = name
        if display_name:
            params['displayName'] = display_name
        if desc:
            params['desc'] = desc
        if website:
            params['website'] = website
            
        response = requests.put(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_workspace_boards(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Get all boards in a workspace
        
        Args:
            workspace_id (str): ID of the workspace
            
        Returns:
            List[Dict[str, Any]]: List of board details
        """
        endpoint = f"{self.BASE_URL}/organizations/{workspace_id}/boards"
        params = {
            **self.auth_params,
            'fields': 'all'
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_board_members(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Get all members of a board
        
        Args:
            board_id (str): ID of the board
            
        Returns:
            List[Dict[str, Any]]: List of member details
        """
        endpoint = f"{self.BASE_URL}/boards/{board_id}/members"
        params = {
            **self.auth_params,
            'fields': 'id,fullName,username'
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_workspace_members(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Get all members of a workspace
        
        Args:
            workspace_id (str): ID of the workspace
            
        Returns:
            List[Dict[str, Any]]: List of member details with their membership info
        """
        endpoint = f"{self.BASE_URL}/organizations/{workspace_id}/members"
        params = {
            **self.auth_params,
            'fields': 'id,fullName,username,email'
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_workspace_memberships(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Get all memberships (members with their roles) of a workspace
        
        Args:
            workspace_id (str): ID of the workspace
            
        Returns:
            List[Dict[str, Any]]: List of memberships with member details and their type/role
        """
        endpoint = f"{self.BASE_URL}/organizations/{workspace_id}/memberships"
        params = {
            **self.auth_params,
            'member': 'true',
            'member_fields': 'id,fullName,username'
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def add_member_to_workspace(
        self, 
        workspace_id: str, 
        member_id: str,
        member_type: str = 'normal'
    ) -> Dict[str, Any]:
        """
        Add a member to a workspace by member ID
        
        Args:
            workspace_id (str): ID of the workspace
            member_id (str): ID of the member to add
            member_type (str): Type of membership ('normal' or 'admin')
            
        Returns:
            Dict[str, Any]: Membership details
        """
        endpoint = f"{self.BASE_URL}/organizations/{workspace_id}/members/{member_id}"
        params = {
            **self.auth_params,
            'type': member_type
        }
        
        response = requests.put(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def add_all_board_members_to_workspace(self, workspace_id: str, member_type: str = 'admin') -> Dict[str, Any]:
        """
        Get all members from all boards in a workspace and add them as workspace members
        
        Args:
            workspace_id (str): ID of the workspace
            member_type (str): Type of membership to assign ('normal' or 'admin')
            
        Returns:
            Dict[str, Any]: Summary of the operation
        """
        # Get all boards in workspace
        boards = self.get_workspace_boards(workspace_id)
        
        # Get all unique members from all boards
        all_members = {}
        for board in boards:
            board_name = board.get('name', 'Unknown Board')
            print(f"  Checking board: {board_name}")
            members = self.get_board_members(board['id'])
            for member in members:
                member_id = member.get('id')
                if member_id and member_id not in all_members:
                    all_members[member_id] = member
        
        # Get existing workspace members
        workspace_members = self.get_workspace_members(workspace_id)
        workspace_member_ids = {member['id'] for member in workspace_members}
        
        results = {
            'total': len(all_members),
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
        
        print(f"\nFound {len(all_members)} unique members across all boards")
        print(f"Promoting members to workspace {member_type}s...\n")
        
        for member_id, member in all_members.items():
            member_name = member.get('fullName', member.get('username', 'Unknown'))
            
            # Skip if already a workspace member
            if member_id in workspace_member_ids:
                print(f"  ⊘ Skipped {member_name} (already workspace member)")
                results['skipped'] += 1
                continue
            
            try:
                # Add as workspace member
                self.add_member_to_workspace(workspace_id, member_id, member_type)
                print(f"  ✓ Added {member_name} as {member_type}")
                results['successful'] += 1
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"  ⊘ Skipped {member_name} (permission denied)")
                    results['skipped'] += 1
                else:
                    error_msg = f"Failed to add {member_name}: {str(e)}"
                    print(f"  ✗ {error_msg}")
                    results['failed'] += 1
                    results['errors'].append(error_msg)
            except Exception as e:
                error_msg = f"Failed to add {member_name}: {str(e)}"
                print(f"  ✗ {error_msg}")
                results['failed'] += 1
                results['errors'].append(error_msg)
        
        return results
    
    def copy_workspace_members(self, source_workspace_id: str, target_workspace_id: str) -> Dict[str, Any]:
        """
        Copy all members from one workspace to another, preserving their roles
        
        Args:
            source_workspace_id (str): ID of the source workspace
            target_workspace_id (str): ID of the target workspace
            
        Returns:
            Dict[str, Any]: Summary of the operation (total, successful, failed)
        """
        # Get memberships from source workspace (includes member info and their type)
        source_memberships = self.get_workspace_memberships(source_workspace_id)
        
        # Get existing members in target workspace to avoid duplicates
        target_members = self.get_workspace_members(target_workspace_id)
        target_member_ids = {member['id'] for member in target_members}
        
        results = {
            'total': len(source_memberships),
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
        
        print(f"Found {len(source_memberships)} members in source workspace")
        
        for membership in source_memberships:
            member = membership.get('member', {})
            member_type = membership.get('memberType', 'normal')
            member_id = member.get('id')
            member_name = member.get('fullName', member.get('username', 'Unknown'))
            
            if not member_id:
                results['failed'] += 1
                continue
            
            # Skip if member already exists in target workspace
            if member_id in target_member_ids:
                print(f"  ⊘ Skipped {member_name} (already in workspace)")
                results['skipped'] += 1
                continue
            
            try:
                # Add member to target workspace with same role
                self.add_member_to_workspace(target_workspace_id, member_id, member_type)
                print(f"  ✓ Added {member_name} as {member_type}")
                results['successful'] += 1
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    # Member might already exist or permission issue
                    print(f"  ⊘ Skipped {member_name} (permission denied - might already be a member)")
                    results['skipped'] += 1
                else:
                    error_msg = f"Failed to add {member_name}: {str(e)}"
                    print(f"  ✗ {error_msg}")
                    results['failed'] += 1
                    results['errors'].append(error_msg)
            except Exception as e:
                error_msg = f"Failed to add {member_name}: {str(e)}"
                print(f"  ✗ {error_msg}")
                results['failed'] += 1
                results['errors'].append(error_msg)
        
        return results