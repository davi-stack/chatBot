# import os.path
# import csv
# from io import StringIO
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# # The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = "1EaneTs3DF1w_C6X9Q7T-alyDVqHEfX1V6R2ciTTp6cU"
# SAMPLE_RANGE_NAME = "Folha1!A1:E15"


# class SheetManipulator:
#     def __init__(self, service):
#         self.service = service

#     def get_spreadsheet_id(self, spreadsheet_name):
#         try:
#             results = self.service.files().list(q=f"name='{spreadsheet_name}'",
#                                                 fields="files(id, name)").execute()
#             spreadsheets = results.get("files", [])

#             if spreadsheets:
#                 return spreadsheets[0]['id']
#             else:
#                 print(f"A planilha '{spreadsheet_name}' não foi encontrada.")
#                 return None

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")
#             return None

#     def create_sheet_per_name(self, spreadsheet_name, sheet_name):
#         spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)
#         if spreadsheet_id:
#             self.create_sheet(spreadsheet_id, sheet_name)
    
#     def create_sheet(self, spreadsheet_id, sheet_name):
#         try:
#             spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

#             # Verifica se a página já existe
#             sheet_id = None
#             sheets = spreadsheet.get('sheets', [])
#             for sheet in sheets:
#                 if sheet['properties']['title'] == sheet_name:
#                     sheet_id = sheet['properties']['sheetId']
#                     break

#             # Se a página não existir, cria uma nova
#             if not sheet_id:
#                 add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
#                 self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
#                 spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#                 sheets = spreadsheet.get('sheets', [])
#                 for sheet in sheets:
#                     if sheet['properties']['title'] == sheet_name:
#                         sheet_id = sheet['properties']['sheetId']
#                         break

#             print(f"Folha '{sheet_name}' criada com sucesso.")

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")

#     def create_spreadsheet(self, spreadsheet_name):
#         try:
#             spreadsheet_body = {'properties': {'title': spreadsheet_name}}
#             spreadsheet = self.service.spreadsheets().create(body=spreadsheet_body).execute()
#             spreadsheet_id = spreadsheet['spreadsheetId']

#             print(f"Planilha '{spreadsheet_name}' criada com sucesso. ID: {spreadsheet_id}")

#             return spreadsheet_id

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")
#             return None

#     def parse_csv_string(self, csv_string):
#         csv_file = StringIO(csv_string)
#         csv_reader = csv.reader(csv_file)
#         data_list = list(csv_reader)

#         return data_list

#     def update_or_create_sheet(self, spreadsheet_name, sheet_name, data):
#         try:
#             spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

#             # Se a planilha não existir, cria uma nova
#             if not spreadsheet_id:
#                 spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

#             # Verifica se a página existe
#             sheet_id = None
#             spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#             sheets = spreadsheet.get('sheets', [])
#             for sheet in sheets:
#                 if sheet['properties']['title'] == sheet_name:
#                     sheet_id = sheet['properties']['sheetId']
#                     break

#             # Se a página não existir, cria uma nova
#             if not sheet_id:
#                 add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
#                 self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
#                 spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#                 sheets = spreadsheet.get('sheets', [])
#                 for sheet in sheets:
#                     if sheet['properties']['title'] == sheet_name:
#                         sheet_id = sheet['properties']['sheetId']
#                         break

#             # Atualiza a página com os dados fornecidos
#             update_data_request = {
#                 'updateCells': {
#                     'start': {'sheetId': sheet_id, 'rowIndex': 0, 'columnIndex': 0},
#                     'rows': [{'values': [{'userEnteredValue': {'stringValue': str(cell)}} for cell in row]} for row in data],
#                     'fields': 'userEnteredValue'
#                 }
#             }
#             self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [update_data_request]}).execute()

#             print(f"Planilha '{spreadsheet_name}', Página '{sheet_name}' atualizada com sucesso.")

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")


# def main():
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("sheets", "v4", credentials=creds)

#         shets = SheetManipulator(service)

#         csv_string = "Nome,Idade,Cargo\nJoão,30,Desenvolvedor\nMaria,25,Designer\nCarlos,35,Gerente"
#         parsed_data = shets.parse_csv_string(csv_string)
#         data = [
#             ['Nome', 'Idade', 'Cargo'],
#             ['João', 30, 'Desenvolvedor'],
#             ['Maria', 25, 'Designer'],
#             ['Carlos', 35, 'Gerente']
#         ]

#         for it in parsed_data:
#             print(it)

#         shets.create_sheet_per_name("AndreTeste", "Folha2")
#     except HttpError as err:
#         print(err)


# if __name__ == "__main__":
#     main()



























# import os.path
# import csv
# from io import StringIO
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# # The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = "1EaneTs3DF1w_C6X9Q7T-alyDVqHEfX1V6R2ciTTp6cU"
# SAMPLE_RANGE_NAME = "Folha1!A1:E15"


# class SheetManipulator:
#     def __init__(self):
#         creds = None

#         if os.path.exists("token.json"):
#             creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#                 creds = flow.run_local_server(port=0)
#             with open("token.json", "w") as token:
#                 token.write(creds.to_json())

#         try:
#             service = build("sheets", "v4", credentials=creds)
#         except HttpError as err:
#             print(err)

#     def edit_sheet(self, spreadsheet_name, sheet_name, data):
#         try:
#             spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

#             # Se a planilha não existir, cria uma nova
#             if not spreadsheet_id:
#                 spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

#             # Verifica se a página existe
#             sheet_id = None
#             spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#             sheets = spreadsheet.get('sheets', [])
#             for sheet in sheets:
#                 if sheet['properties']['title'] == sheet_name:
#                     sheet_id = sheet['properties']['sheetId']
#                     break

#             # Se a página não existir, cria uma nova
#             if not sheet_id:
#                 add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
#                 self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
#                 spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#                 sheets = spreadsheet.get('sheets', [])
#                 for sheet in sheets:
#                     if sheet['properties']['title'] == sheet_name:
#                         sheet_id = sheet['properties']['sheetId']
#                         break

#             # Edita a página com os dados fornecidos
#             update_data_request = {
#                 'updateCells': {
#                     'start': {'sheetId': sheet_id, 'rowIndex': 0, 'columnIndex': 0},
#                     'rows': [{'values': [{'userEnteredValue': {'stringValue': str(cell)}} for cell in row]} for row in data],
#                     'fields': 'userEnteredValue'
#                 }
#             }
#             self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [update_data_request]}).execute()

#             print(f"Planilha '{spreadsheet_name}', Página '{sheet_name}' editada com sucesso.")

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")


#     def get_spreadsheet_id(self, spreadsheet_name):
#         try:
#             results = self.service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
#             sheets = results.get('sheets', [])

#             for sheet in sheets:
#                 if sheet['properties']['title'] == spreadsheet_name:
#                     return SAMPLE_SPREADSHEET_ID

#             print(f"A planilha '{spreadsheet_name}' não foi encontrada.")
#             return None

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")
#             return None

#     def create_sheet_per_name(self, spreadsheet_name, sheet_name):
#         spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)
#         if spreadsheet_id:
#             self.create_sheet(spreadsheet_id, sheet_name)

#     def create_sheet(self, spreadsheet_id, sheet_name):
#         try:
#             spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

#             # Verifica se a página já existe
#             sheet_id = None
#             sheets = spreadsheet.get('sheets', [])
#             for sheet in sheets:
#                 if sheet['properties']['title'] == sheet_name:
#                     sheet_id = sheet['properties']['sheetId']
#                     break

#             # Se a página não existir, cria uma nova
#             if not sheet_id:
#                 add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
#                 self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
#                 spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#                 sheets = spreadsheet.get('sheets', [])
#                 for sheet in sheets:
#                     if sheet['properties']['title'] == sheet_name:
#                         sheet_id = sheet['properties']['sheetId']
#                         break

#             print(f"Folha '{sheet_name}' criada com sucesso.")

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")

#     def create_spreadsheet(self, spreadsheet_name):
#         try:
#             spreadsheet_body = {'properties': {'title': spreadsheet_name}}
#             spreadsheet = self.service.spreadsheets().create(body=spreadsheet_body).execute()
#             spreadsheet_id = spreadsheet['spreadsheetId']

#             print(f"Planilha '{spreadsheet_name}' criada com sucesso. ID: {spreadsheet_id}")

#             return spreadsheet_id

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")
#             return None

#     def parse_csv_string(self, csv_string):
#         csv_file = StringIO(csv_string)
#         csv_reader = csv.reader(csv_file)
#         data_list = list(csv_reader)

#         return data_list

#     def update_or_create_sheet(self, spreadsheet_name, sheet_name, data):
#         try:
#             spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

#             # Se a planilha não existir, cria uma nova
#             if not spreadsheet_id:
#                 spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

#             # Verifica se a página existe
#             sheet_id = None
#             spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#             sheets = spreadsheet.get('sheets', [])
#             for sheet in sheets:
#                 if sheet['properties']['title'] == sheet_name:
#                     sheet_id = sheet['properties']['sheetId']
#                     break

#             # Se a página não existir, cria uma nova
#             if not sheet_id:
#                 add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
#                 self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
#                 spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#                 sheets = spreadsheet.get('sheets', [])
#                 for sheet in sheets:
#                     if sheet['properties']['title'] == sheet_name:
#                         sheet_id = sheet['properties']['sheetId']
#                         break

#             # Atualiza a página com os dados fornecidos
#             update_data_request = {
#                 'updateCells': {
#                     'start': {'sheetId': sheet_id, 'rowIndex': 0, 'columnIndex': 0},
#                     'rows': [{'values': [{'userEnteredValue': {'stringValue': str(cell)}} for cell in row]} for row in data],
#                     'fields': 'userEnteredValue'
#                 }
#             }
#             self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [update_data_request]}).execute()

#             print(f"Planilha '{spreadsheet_name}', Página '{sheet_name}' atualizada com sucesso.")

#         except HttpError as err:
#             print(f"Um erro ocorreu: {err}")

# def main():
#     creds = None

#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("sheets", "v4", credentials=creds)

#         sheet = service.spreadsheets()
#         result = (
#             sheet.values()
#             .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
#             .execute()
#         )
#         values = result.get("values", [])

#         if not values:
#             print("No data found.")
#             return

#         shets = SheetManipulator(service)

#         # Teste 1: Criar uma nova planilha
#         new_spreadsheet_name = "NovaPlanilhaTeste"
#         new_spreadsheet_id = shets.create_spreadsheet(new_spreadsheet_name)
#         print(f"Teste 1 - Nova planilha criada. ID: {new_spreadsheet_id}")

#         # Teste 2: Criar uma nova folha em uma planilha existente
#         new_sheet_name = "NovaFolhaTeste"
#         shets.create_sheet(new_spreadsheet_id, new_sheet_name)
#         print(f"Teste 2 - Nova folha criada na planilha '{new_spreadsheet_name}'")

#         # Teste 3: Editar uma folha existente
#         edit_data = [
#             ['Nome', 'Idade', 'Cargo'],
#             ['João Editado', 31, 'Desenvolvedor Editado'],
#             ['Maria Editada', 26, 'Designer Editada'],
#             ['Carlos Editado', 36, 'Gerente Editado']
#         ]
#         shets.edit_sheet(new_spreadsheet_name, new_sheet_name, edit_data)
#         print(f"Teste 3 - Folha '{new_sheet_name}' editada na planilha '{new_spreadsheet_name}'")

#         # Teste 4: Atualizar ou criar uma folha
#         data_to_update_or_create = [
#             ['Nome', 'Idade', 'Cargo'],
#             ['João Novo', 32, 'Desenvolvedor Novo'],
#             ['Maria Nova', 27, 'Designer Nova'],
#             ['Carlos Novo', 37, 'Gerente Novo']
#         ]
#         shets.update_or_create_sheet(new_spreadsheet_name, new_sheet_name, data_to_update_or_create)
#         print(f"Teste 4 - Folha '{new_sheet_name}' atualizada ou criada na planilha '{new_spreadsheet_name}'")

#     except HttpError as err:
#         print(err)


# if __name__ == "__main__":
#     main()







































import os.path
import csv
from io import StringIO
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1EaneTs3DF1w_C6X9Q7T-alyDVqHEfX1V6R2ciTTp6cU"
SAMPLE_RANGE_NAME = "Sheet1!A1:"

class SheetManipulator:
    def __init__(self):
        self.creds = None

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        try:
            # Build the Sheets API service
            self.service = build("sheets", "v4", credentials=self.creds)
        except HttpError as err:
            print(err)

        except HttpError as err:
            print(f"Um erro ocorreu: {err}")
            return None
    # def conditional_formatting(self, spreadsheet_name, sheet_name, config_json):
    #     spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

    #     if not spreadsheet_id:
    #         spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

    #     # Verificar se a aba existe
    #     sheet_id = None
    #     spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    #     sheets = spreadsheet.get('sheets', [])
        
    #     for sheet in sheets:
    #         if sheet['properties']['title'] == sheet_name:
    #             sheet_id = sheet['properties']['sheetId']
    #             break

    #     # Se a aba não existe, criar uma nova
    #     if not sheet_id:
    #         add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
    #         self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
    #         spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    #         sheets = spreadsheet.get('sheets', [])
            
    #         for sheet in sheets:
    #             if sheet['properties']['title'] == sheet_name:
    #                 sheet_id = sheet['properties']['sheetId']
    #                 break

    #     my_range = {
    #         "sheetId": sheet_id,
    #         "startRowIndex": 1,
    #         "endRowIndex": 11,
    #         "startColumnIndex": 0,
    #         "endColumnIndex": 4,
    #     }

    #     requests = []

    #     for rule_config in config_json:
    #         condition_type = rule_config["condition_type"]
    #         user_entered_value = rule_config["user_entered_value"]
    #         format_config = rule_config["format_config"]

    #         rule = {
    #             "ranges": [my_range],
    #             "booleanRule": {
    #                 "condition": {
    #                     "type": condition_type,
    #                     "values": [{"userEnteredValue": user_entered_value}],
    #                 },
    #                 "format": format_config,
    #             },
    #         }

    #         add_rule_request = {
    #             "addConditionalFormatRule": {"rule": rule, "index": 0}
    #         }

    #         requests.append(add_rule_request)

    #     body = {"requests": requests}

    #     try:
    #         response = (
    #             self.service.spreadsheets()
    #             .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    #             .execute()
    #         )
    #         print(f"{len(response.get('replies'))} cells updated.")
    #         return response

    #     except HttpError as error:
    #         print(f"An error occurred: {error}")
    #         return error

    def create_or_edit_sheet_with_json_and_format(self, json_data):
        try:
            # Extrair dados do JSON
            json_data = json.loads(json_data)
            spreadsheet_name = json_data.get('spreadsheet_name')
            sheet_name = json_data.get('sheet_name')
            data = json_data.get('data', [])

            spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

            # Se a planilha não existe, criar uma nova
            if not spreadsheet_id:
                spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

            # Verificar se a aba existe
            sheet_id = None
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = spreadsheet.get('sheets', [])
            for sheet in sheets:
                if sheet['properties']['title'] == sheet_name:
                    sheet_id = sheet['properties']['sheetId']
                    break

            # Se a aba não existe, criar uma nova
            if not sheet_id:
                add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
                self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
                spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
                sheets = spreadsheet.get('sheets', [])
                for sheet in sheets:
                    if sheet['properties']['title'] == sheet_name:
                        sheet_id = sheet['properties']['sheetId']
                        break

            # Editar a planilha com os dados fornecidos
            requests = []

            for item in data:
                if 'range' in item and 'values' in item:
                    range_ = item['range']
                    values = item['values']
                    cell_format = item.get('cell_format', {})
                    formula = item.get('formula', '')
                    merge_cells = item.get('merge_cells', False)

                    # Adicionar valores à solicitação
                    values_request = [{'userEnteredValue': {'stringValue': str(value)}} for value in values]
                    requests.append({
                        'updateCells': {
                            'range': range_,
                            'fields': 'userEnteredValue, userEnteredFormat',
                            'rows': [{'values': values_request, 'format': {'textFormat': cell_format}}],
                        }
                    })

                    # Adicionar fórmula se presente
                    if formula:
                        requests[-1]['updateCells']['rows'][0]['values'][0]['userEnteredValue'] = {'formulaValue': formula}

                    # Mesclar células se necessário
                    if merge_cells:
                        requests.append({
                            'mergeCells': {
                                'range': range_,
                                'mergeType': 'MERGE_ALL'
                            }
                        })

            # Solicitação enviada
            self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()

            # Obter o link da planilha editada
            spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            print(f"Spreadsheet '{spreadsheet_name}', Sheet '{sheet_name}' edited successfully.")
            print(f"Spreadsheet URL: {spreadsheet_url}")

            return spreadsheet_url

        except HttpError as err:
            print(f"An error occurred: {err}")
            return None
   
   
   
   
    def create_spreadsheet(self, spreadsheet_name):
        try:
            spreadsheet_body = {'properties': {'title': spreadsheet_name}}
            spreadsheet = self.service.spreadsheets().create(body=spreadsheet_body).execute()
            spreadsheet_id = spreadsheet['spreadsheetId']

            print(f"Planilha '{spreadsheet_name}' criada com sucesso. ID: {spreadsheet_id}")

            return spreadsheet_id

        except HttpError as err:
            print(f"Um erro ocorreu: {err}")
            return None

    def parse_csv_string(self, csv_string):
        csv_file = StringIO(csv_string)
        csv_reader = csv.reader(csv_file)
        data_list = list(csv_reader)

        return data_list
    # def get_spreadsheet_id(self, spreadsheet_name):
    #     try:
    #         results = self.service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    #         sheets = results.get('sheets', [])

    #         for sheet in sheets:
    #             if sheet['properties']['title'] == spreadsheet_name:
    #                 return SAMPLE_SPREADSHEET_ID

    #         print(f"A planilha '{spreadsheet_name}' não foi encontrada.")
    #         return None

    #     except HttpError as err:
    #         print(f"Um erro ocorreu: {err}")
    #         return None
    
    def get_spreadsheet_id(self, spreadsheet_name):
        try:
            spreadsheet_list = self.service.spreadsheets().list().execute()
            spreadsheets = spreadsheet_list.get('files', [])

            for spreadsheet in spreadsheets:
                if spreadsheet['name'] == spreadsheet_name:
                    return spreadsheet['id']

            print(f"A planilha '{spreadsheet_name}' não foi encontrada.")
            return None

        except HttpError as err:
            print(f"Um erro ocorreu: {err}")
            return None

    def create_or_edit_sheet_with_json(self, json_data):
        try:
            # Extrair dados do JSON
            json_data = json.loads(json_data)
            spreadsheet_name = json_data.get('spreadsheet_name')
            sheet_name = json_data.get('sheet_name')
            data = json_data.get('data', [])

            spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

            # Se a planilha não existe, criar uma nova
            if not spreadsheet_id:
                spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

            # Verificar se a aba existe
            sheet_id = None
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = spreadsheet.get('sheets', [])
            for sheet in sheets:
                if sheet['properties']['title'] == sheet_name:
                    sheet_id = sheet['properties']['sheetId']
                    break

            # Se a aba não existe, criar uma nova
            if not sheet_id:
                add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
                self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
                spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
                sheets = spreadsheet.get('sheets', [])
                for sheet in sheets:
                    if sheet['properties']['title'] == sheet_name:
                        sheet_id = sheet['properties']['sheetId']
                        break

            # Editar a planilha com os dados fornecidos
            requests = []

            for row_index, row_data in enumerate(data, start=1):
                row_values = [{'userEnteredValue': {'stringValue': str(value)}} for value in row_data.values()]
                requests.append({
                    'updateCells': {
                        'start': {'sheetId': sheet_id, 'rowIndex': row_index, 'columnIndex': 0},
                        'rows': [{'values': row_values}],
                        'fields': 'userEnteredValue'
                    }
                })

            self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()

            # Obter o link da planilha editada
            spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            print(f"Spreadsheet '{spreadsheet_name}', Sheet '{sheet_name}' edited successfully.")
            print(f"Spreadsheet URL: {spreadsheet_url}")

            return spreadsheet_url

        except HttpError as err:
            print(f"An error occurred: {err}")
            return None
    
    # def create_or_edit_sheet_with_json(self, json_data):
    #     try:
    #         # Extrair dados do JSON
    #         json_data = json.loads(json_data)
    #         spreadsheet_name = json_data.get('spreadsheet_name')
    #         sheet_name = json_data.get('sheet_name')
    #         data = json_data.get('data', [])

    #         spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

    #         # Se a planilha não existe, criar uma nova
    #         if not spreadsheet_id:
    #             spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

    #         # Verificar se a aba existe
    #         sheet_id = None
    #         spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    #         sheets = spreadsheet.get('sheets', [])
    #         for sheet in sheets:
    #             if sheet['properties']['title'] == sheet_name:
    #                 sheet_id = sheet['properties']['sheetId']
    #                 break

    #         # Se a aba não existe, criar uma nova
    #         if not sheet_id:
    #             add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
    #             self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
    #             spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    #             sheets = spreadsheet.get('sheets', [])
    #             for sheet in sheets:
    #                 if sheet['properties']['title'] == sheet_name:
    #                     sheet_id = sheet['properties']['sheetId']
    #                     break

    #         # Editar a planilha com os dados fornecidos
    #         requests = []

    #         for item in data:
    #             if 'range' in item:
    #                 range_ = item['range']
    #                 cell_format = item.get('cell_format', {})

    #                 if 'cell_formula' in item:
    #                     # Se houver uma fórmula, adicioná-la à solicitação
    #                     requests.append({
    #                         'updateCells': {
    #                             'range': range_,
    #                             'fields': 'userEnteredValue,note',
    #                             'rows': [{'values': [{'userEnteredValue': {'formulaValue': item['cell_formula']}}]}],
    #                             'cell': {'note': item.get('note', ''), 'userEnteredFormat': cell_format}
    #                         }
    #                     })
    #                 else:
    #                     # Se não houver uma fórmula, adicionar valores à solicitação
    #                     values = [{'userEnteredValue': {'stringValue': str(value)}} for value in item.values() if value not in ('merge_cells', 'cell_format')]
    #                     requests.append({
    #                         'updateCells': {
    #                             'range': range_,
    #                             'fields': 'userEnteredValue,note',
    #                             'rows': [{'values': values}],
    #                             'cell': {'note': item.get('note', ''), 'userEnteredFormat': cell_format}
    #                         }
    #                     })

    #                 # Mesclar células se necessário
    #                 if item.get('merge_cells'):
    #                     requests.append({
    #                         'mergeCells': {
    #                             'range': range_,
    #                             'mergeType': 'MERGE_ALL'
    #                         }
    #                     })

    #         # Solicitação enviada fora do loop
    #         self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()

    #         # Obter o link da planilha editada
    #         spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
    #         print(f"Spreadsheet '{spreadsheet_name}', Sheet '{sheet_name}' edited successfully.")
    #         print(f"Spreadsheet URL: {spreadsheet_url}")

    #         return spreadsheet_url

    #     except HttpError as err:
    #         print(f"An error occurred: {err}")
    #         return None


    

     
    # def edit_sheet_with_json(self, json_data):
    #     try:
    #         # Extract metadata from JSON
    #         json_data = json.loads(json_data)
    #         spreadsheet_name = json_data.get('spreadsheet_name', '')
    #         sheet_name = json_data.get('sheet_name', '')

    #         # If either spreadsheet_name or sheet_name is missing, print an error and return
    #         if not spreadsheet_name or not sheet_name:
    #             print("Error: Missing spreadsheet_name or sheet_name in JSON.")
    #             return

    #         # Get or create the spreadsheet
    #         spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)
    #         if not spreadsheet_id:
    #             spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

    #         # Check if the sheet exists, create a new one if not
    #         sheet_id = self.get_or_create_sheet(spreadsheet_id, sheet_name)

    #         # Extract sheet data from JSON
    #         data = json_data.get('data', [])

    #         # Update the sheet with the provided data
    #         update_data_request = {
    #             'updateCells': {
    #                 'start': {'sheetId': sheet_id, 'rowIndex': 0, 'columnIndex': 0},
    #                 'rows': [{'values': [{'userEnteredValue': {'stringValue': str(cell)}} for cell in row]} for row in data],
    #                 'fields': 'userEnteredValue'
    #             }
    #         }
    #         self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [update_data_request]}).execute()

    #         print(f"Spreadsheet '{spreadsheet_name}', Sheet '{sheet_name}' edited successfully.")

    #     except HttpError as err:
    #         print(f"An error occurred: {err}")

   

    
    def edit_sheet(self, spreadsheet_name, sheet_name, data):
        try:
            spreadsheet_id = self.get_spreadsheet_id(spreadsheet_name)

            # If the spreadsheet doesn't exist, create a new one
            if not spreadsheet_id:
                spreadsheet_id = self.create_spreadsheet(spreadsheet_name)

            # Check if the sheet exists
            sheet_id = None
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = spreadsheet.get('sheets', [])
            for sheet in sheets:
                if sheet['properties']['title'] == sheet_name:
                    sheet_id = sheet['properties']['sheetId']
                    break

            # If the sheet doesn't exist, create a new one
            if not sheet_id:
                add_sheet_request = {'addSheet': {'properties': {'title': sheet_name}}}
                self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [add_sheet_request]}).execute()
                spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
                sheets = spreadsheet.get('sheets', [])
                for sheet in sheets:
                    if sheet['properties']['title'] == sheet_name:
                        sheet_id = sheet['properties']['sheetId']
                        break

            # Edit the sheet with the provided data
            update_data_request = {
                'updateCells': {
                    'start': {'sheetId': sheet_id, 'rowIndex': 0, 'columnIndex': 0},
                    'rows': [{'values': [{'userEnteredValue': {'stringValue': str(cell)}} for cell in row]} for row in data],
                    'fields': 'userEnteredValue'
                }
            }
            self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': [update_data_request]}).execute()

            print(f"Spreadsheet '{spreadsheet_name}', Sheet '{sheet_name}' edited successfully.")

        except HttpError as err:
            print(f"An error occurred: {err}")

    # ... (similar refactoring for other methods)
    def batch_update_values(self, id, range_name, value_input_option, values):
        try:
            data = [{"range": range_name, "values": values}]
            body = {"valueInputOption": value_input_option, "data": data}
            result = (
                self.service.spreadsheets()
                .values()
                .batchUpdate(spreadsheetId=id, body=body)
                .execute()
            )
            print(f"{(result.get('totalUpdatedCells'))} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    # def conditional_formatting(self, spreadsheet_id):
    #     my_range = {
    #         "sheetId": 0,
    #         "startRowIndex": 1,
    #         "endRowIndex": 11,
    #         "startColumnIndex": 0,
    #         "endColumnIndex": 4,
    #     }
    #     requests = [
    #         {
    #             "addConditionalFormatRule": {
    #                 "rule": {
    #                     "ranges": [my_range],
    #                     "booleanRule": {
    #                         "condition": {
    #                             "type": "CUSTOM_FORMULA",
    #                             "values": [
    #                                 {
    #                                     "userEnteredValue": (
    #                                         "=GT($D2,median($D$2:$D$11))"
    #                                     )
    #                                 }
    #                             ],
    #                         },
    #                         "format": {
    #                             "textFormat": {"foregroundColor": {"red": 0.8}}
    #                         },
    #                     },
    #                 },
    #                 "index": 0,
    #             }
    #         },
    #         {
    #             "addConditionalFormatRule": {
    #                 "rule": {
    #                     "ranges": [my_range],
    #                     "booleanRule": {
    #                         "condition": {
    #                             "type": "CUSTOM_FORMULA",
    #                             "values": [
    #                                 {
    #                                     "userEnteredValue": (
    #                                         "=LT($D2,median($D$2:$D$11))"
    #                                     )
    #                                 }
    #                             ],
    #                         },
    #                         "format": {
    #                             "backgroundColor": {
    #                                 "red": 1,
    #                                 "green": 0.4,
    #                                 "blue": 0.4,
    #                             }
    #                         },
    #                     },
    #                 },
    #                 "index": 0,
    #             }
    #         },
    #     ]
    #     body = {"requests": requests}
    #     response = (
    #         self.service.spreadsheets()
    #         .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    #         .execute()
    #     )
    #     print(f"{(len(response.get('replies')))} cells updated.")
    #     return response


def conditional_formatting(spreadsheet_id, creds):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)

    my_range = {
        "sheetId": 0,
        "startRowIndex": 1,
        "endRowIndex": 11,
        "startColumnIndex": 0,
        "endColumnIndex": 4,
    }
    requests = [
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [my_range],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {
                                    "userEnteredValue": (
                                        "=GT($D2,median($D$2:$D$11))"
                                    )
                                }
                            ],
                        },
                        "format": {
                            "textFormat": {"foregroundColor": {"red": 0.8}}
                        },
                    },
                },
                "index": 0,
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [my_range],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {
                                    "userEnteredValue": (
                                        "=LT($D2,median($D$2:$D$11))"
                                    )
                                }
                            ],
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 1,
                                "green": 0.4,
                                "blue": 0.4,
                            }
                        },
                    },
                },
                "index": 0,
            }
        },
    ]
    body = {"requests": requests}
    response = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
    print(f"{(len(response.get('replies')))} cells updated.")
    return response

  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def main():
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    # ... (other code using the service object)

    # Example conditional formatting usage
    configuration = [
        {
            "condition_type": "CUSTOM_FORMULA",
            "user_entered_value": "=AND(ISNUMBER(D2), D2 > MEDIAN(D$2:D$11))",
            "format_config": {"textFormat": {"foregroundColor": {"red": 0.8}}},
        },
        {
            "condition_type": "CUSTOM_FORMULA",
            "user_entered_value": "=AND(ISNUMBER(D2), D2 < MEDIAN(D$2:D$11))",
            "format_config": {"backgroundColor": {"red": 1, "green": 0.4, "blue": 0.4}},
        },
    ]

    spreadsheet_id = "your_spreadsheet_id"  # Replace with actual ID
    conditional_formatting(spreadsheet_id, creds)
# def main():
#     creds = None

#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("sheets", "v4", credentials=creds)

#         # sheet = service.spreadsheets()
#         # result = (
#         #     sheet.values()
#         #     .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
#         #     .execute()
#         # )
#         # values = result.get("values", [])

#         # if not values:
#         #     print("No data found.")
#         #     return

#         sheet_manipulator = SheetManipulator()
#         json_dat = """{
#   "spreadsheet_name": "Test_Spreadsheet",
#   "sheet_name": "Test_Sheet",
#   "data": [
#     {"range": "A1:C1", "values": ["Title A1", "Title B1", "Title C1"], "cell_format": {"textFormat": {"bold": true}}},
#     {"range": "A2:C4", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9], "merge_cells": true, "cell_format": {"backgroundColor": {"red": 1, "green": 0.8, "blue": 0.8}}},
#     {"range": "B2:B4", "number_format": {"type": "PERCENT", "pattern": "#,##0.00%"}, "cell_format": {"backgroundColor": {"red": 0.8, "green": 1, "blue": 0.8}}},
#     {"range": "C2:C4", "formula": "=SUM(A2:B2)", "cell_format": {"backgroundColor": {"red": 0.8, "green": 0.8, "blue": 1}}}
#   ]
# }"""
#         #sheet_manipulator.create_or_edit_sheet_with_json_and_format(json_dat)
#         # ... (similar refactoring for the main part)
#          #     sheet_manipulator.batch_update_values(
#          #     "1-tH9E0uHToCPePY5T6QQheW6jCvBcvPYUkf_KthnWGc",
#          #     "A1:C2",
#         #     "USER_ENTERED",
#         #     [["F", "B"], ["C", "D"]],
#         # )
#         # Example JSON configuration
#         configuration = configuration = [
#     {
#         "condition_type": "CUSTOM_FORMULA",
#         "user_entered_value": "=AND(ISNUMBER(D2), D2 > MEDIAN(D$2:D$11))",
#         "format_config": {"textFormat": {"foregroundColor": {"red": 0.8}}},
#     },
#     {
#         "condition_type": "CUSTOM_FORMULA",
#         "user_entered_value": "=AND(ISNUMBER(D2), D2 < MEDIAN(D$2:D$11))",
#         "format_config": {
#             "backgroundColor": {"red": 1, "green": 0.4, "blue": 0.4}
#         },
#     },
# ]
#         id = sheet_manipulator.create_spreadsheet("Teste")
#         conditional_formatting(id, sheet_manipulator.creds)
#         # sheet_manipulator.conditional_formatting(
#         # "Your Spreadsheet Name", "Your Sheet Name", configuration)
#     except HttpError as err:
#         print(err)

# if __name__ == "__main__":
#     main()
def main():
    """
    Tests the conditional_formatting function.
    """

    # Load credentials (replace with your authentication method)
    creds = ...  # Replace with your credential loading logic

    # Specify spreadsheet ID and sheet name
    spreadsheet_id = "your_spreadsheet_id"  # Replace with actual ID
    sheet_name = "Your Sheet Name"

    try:
        # Call conditional_formatting function
        response = conditional_formatting(spreadsheet_id, creds)

        # Print success message or handle errors
        if isinstance(response, dict):
            print(f"Conditional formatting applied successfully. {len(response.get('replies'))} cells updated.")
        else:
            print(f"An error occurred: {response}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()





















# def main():
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("sheets", "v4", credentials=creds)

#         sheet = service.spreadsheets()
#         result = (
#             sheet.values()
#             .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
#             .execute()
#         )
#         values = result.get("values", [])

#         if not values:
#             print("No data found.")
#             return

#         shets = SheetManipulator(service)

#         csv_string = "Nome,Idade,Cargo\nJoão,30,Desenvolvedor\nMaria,25,Designer\nCarlos,35,Gerente"
#         parsed_data = shets.parse_csv_string(csv_string)
#         data = [
#             ['Nome', 'Idade', 'Cargo'],
#             ['João', 30, 'Desenvolvedor'],
#             ['Maria', 25, 'Designer'],
#             ['Carlos', 35, 'Gerente']
#         ]

#         for it in parsed_data:
#             print(it)

#         #shets.update_or_create_sheet("AndreTeste", "Folha1", data)
#         #shets.create_sheet_per_name("AndreTeste", "Folha2")
#         shets.create_spreadsheet("TesteDavi")
#         shets.edit_sheet("TesteDavi", "Folha2", data)
#     except HttpError as err:
#         print(err)


# if __name__ == "__main__":
#     main()
