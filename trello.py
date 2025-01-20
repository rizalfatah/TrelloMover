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