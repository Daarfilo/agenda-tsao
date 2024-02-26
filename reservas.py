import pandas as pd
from sheet_tsao import sheet_api

class Reservas:
    def __init__(self, nombre, personas, habitacion, check_in, check_out, estado):
        self.nombre=str(nombre)
        self.personas=int(personas)
        self.habitacion=str(habitacion)
        self.check_in=pd.to_datetime(check_in, format='%d/%m/%Y').date()
        self.check_out=pd.to_datetime(check_out, format='%d/%m/%Y').date()
        self.estado=bool(estado)

    def get_nombre(self):
        return self.nombre
    def get_personas(self):
        return self.personas
    def get_habitacion(self):
        return self.habitacion
    def get_check_in(self):
        return self.check_in
    def get_check_out(self):
        return self.check_out    
    def get_estado(self):
        return self.estado
    
    def __str__(self) -> str:
        return "{},{},{},{},{},{}".format(self.nombre, self.personas, self.habitacion, self.check_in, self.check_out, self.estado)

def sheet_to_reserva():
    array=[]
    for i, r in sheet_on.descargar().iterrows():
        reserva=Reservas(r.iloc[4], r.iloc[5], r.iloc[3], r.iloc[0], r.iloc[1], r.iloc[2])
        array.append(reserva)
    return array

def show_reservas(obj):
    for res in obj:
        print(res.__str__())

def rango_fechas(checks):
    menor = None
    mayor = None
    for reserva in checks:
        if menor is None or reserva.check_in < menor:
            menor = reserva.check_in
        if mayor is None or reserva.check_out > mayor:
            mayor = reserva.check_out
    return menor, mayor

def df_reservas():
    # Crear un DataFrame vacío con las fechas como índices y las columnas H1, H2, H3
    dates = pd.date_range(*rango_fechas(lista_reservas))
    columns = sorted(list(set(reserva.habitacion for reserva in lista_reservas if reserva.habitacion)))
    df = pd.DataFrame(index=dates, columns=columns)
    # Llenar el DataFrame con los datos y manejar los cruces de fechas
    for row in lista_reservas:
        if row.habitacion:
            name = row.nombre
            header = row.habitacion
            start_date = row.check_in
            end_date = row.check_out
            # Verificar si hay conflictos en las fechas
            conflicted_dates = df.loc[start_date:end_date - pd.Timedelta(days=1), header]
            # Si todas las celdas en conflicto están vacías, se pueden llenar con el nombre
            if conflicted_dates.isna().all():
                df.loc[start_date:end_date - pd.Timedelta(days=1), header] = name
            else:
                # Si hay alguna celda ya ocupada, pero no todas, debe haber un conflicto
                if conflicted_dates.notnull().any() and not (conflicted_dates == name).all():
                    # Reemplazar los valores en conflicto por 'error'
                    df.loc[conflicted_dates.index, header] = 'OVERBOOKING-' + name

    return df

sheet_on=sheet_api()
lista_reservas=sheet_to_reserva()
tabla_reservas=df_reservas()
sheet_on.cargar_hoja(tabla_reservas)