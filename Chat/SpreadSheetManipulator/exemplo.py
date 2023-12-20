import os.path

import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_RANGE_NAME = "Class Data!A2:E"

creds = None

def login():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    cr = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not cr or not cr.valid:
    if cr and cr.expired and cr.refresh_token:
      cr.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      cr = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

def create_spreadsheet_from_csv_string(csv_string, sheet_name):
    """Creates a new spreadsheet from a CSV string.

    Args:
        csv_string: The CSV data as a string.
        sheet_name: The name of the spreadsheet to create.

    Returns:
        The ID of the newly created spreadsheet.
    """

    creds = None
    # ... (authorization code remains the same) ...

    try:
        service = build("sheets", "v4", credentials=creds)

        # Create the spreadsheet.
        sheet = service.spreadsheets().create(
            body={
                "properties": {
                    "title": sheet_name,
                },
                "sheets": [
                    {
                        "properties": {
                            "title": sheet_name,
                        },
                    },
                ],
            }
        ).execute()
        
        # Parse the CSV string into a list of lists.
        reader = csv.reader(csv_string.splitlines())
        data = list(reader)

        # Update the spreadsheet with the CSV data.
        sheet_id = sheet.get("spreadsheetId")
        sheet = service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range="A1", valueInputOption="USER_ENTERED", body={
                "values": data,
            }
        ).execute()

        return sheet_id

    except HttpError as err:
        print(err)

def main():
  creds = login()

  
  csv_string = "column1,column2\nrow1value1,row1value2\nrow2value1,row2value2"
  sheet_name = "My New Sheet"

  sheet_id = create_spreadsheet_from_csv_string(csv_string, sheet_name)
  print(f"Spreadsheet created with ID: {sheet_id}")



if __name__ == "__main__":
  main()