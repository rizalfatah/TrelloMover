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

3. Create a `.env` file in the project root and add your Trello credentials and workspace list:
   ```
   TOKEN=your_token
   API_KEY=your_api_key
   WORKSPACES=["My Private Room", "TDS", "Freelance", "Antrian"]
   ```

## Usage

Run the script and select a workspace from the interactive menu:

```bash
python main.py
```

The script will display a numbered list of workspaces from your `.env` file. Select one by entering its number, and the migration will proceed automatically.

## License

This project is licensed under the MIT License.
