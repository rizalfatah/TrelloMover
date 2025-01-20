# Trello Automation

This project automates the process of moving boards into a new Trello workspace, enabling access to a trial premium workspace.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd TrelloMover
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Trello credentials and workspace names:
   ```
   TOKEN=your_token
   API_KEY=your_api_key
   OLD_WORKSPACE_NAME="Your Old Workspace Name"
   NEW_WORKSPACE_NAME="Your New Workspace Name"
   ```

## Usage

Run the script to start the automation:
```bash
python main.py
```

## License

This project is licensed under the MIT License.
