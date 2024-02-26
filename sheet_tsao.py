import gspread, openpyxl
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class sheet_api:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('disponibilidad-tsao.json', self.scope)
        self.client = gspread.authorize(self.creds)

    def descargar(self):
        sheet = self.client.open('disponibilidad_tsao').sheet1
        reservas = sheet.get_all_records()
        df=pd.json_normalize(reservas)
        
        pattern = r'^(.*?)(?:\n|\s+)(\d+)'
        matches = df['Nombre del huésped'].str.extract(pattern)
        df['Nombre'] = matches[0]
        df['Personas'] = matches[1].fillna(0).astype(int)
        df['Estado'] = df['Estado'].apply(lambda x: True if x == 'OK' else False)
        df.drop(columns=['Nombre del huésped','Habitaciones', 'Fecha de reserva', 'Precio', 'Comisión', 'Número de reserva'], inplace=True)
        return df
    
    def cargar_hoja(self, data):
        data.fillna('', inplace=True)    
        data.index = data.index.astype(str)
        data.reset_index(inplace=True)
        libro = self.client.open('disponibilidad_tsao')
        hoja_existente = libro.worksheet('Cuadro de Reservas')
        hoja_existente.clear()
        datos_lista = [data.columns.tolist()] + data.values.tolist()
        rango_celdas = f"A1:{openpyxl.utils.get_column_letter(data.shape[1] + 1)}{data.shape[0] + 1}"
        hoja_existente.update(rango_celdas, datos_lista)