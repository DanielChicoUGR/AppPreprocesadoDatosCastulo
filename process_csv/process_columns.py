from pathlib import Path

import pandas as pd

from process_csv.listas_tipos_datos import ceramicas_columns, otros_materiales


def process_csv(raw_file_path):
    file_path = Path(raw_file_path)
    folder_path = file_path.parent
    # file_name = file_path.name
    print(f"Procesando archivo CSV: {file_path}")
    try:
        df = pd.read_csv(file_path, encoding="UTF8", sep=";", decimal=",")
        df = processData(df)
        df.to_csv(folder_path / "nuevo_dataset.csv", index=False, sep=";")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")


def processData(df, include_other_materials=False):
    data = remove_unnamed_columns(df)
    data.Nivel = data.Nivel.apply(processnivel)
    data["Codigo_estrato"] = (
        data["Codigo_estrato"].apply(processestrato).astype("string")
    )
    # print("a")
    columnas = ceramicas_columns

    if not include_other_materials:
        temp = data.drop(columns=["Cod Registro"]).drop(columns=otros_materiales)
    else:
        columnas += otros_materiales

    grouped_data = (
        temp.groupby("Codigo_estrato")
        .agg(
            {
                **{col: "sum" for col in columnas},
                **{
                    col: "first"
                    for col in temp.columns
                    if col.startswith(("X", "Y", "Z", "Nivel"))
                },
            }
        )
        .reset_index()
    )
    # Calcular el peso total y el número de piezas por estrato
    columnas_pesos = [col for col in columnas if col.startswith("Peso")]
    columnas_ceramicas = [col for col in columnas if not col.startswith("Peso")]

    grouped_data["Peso_total"] = grouped_data[columnas_pesos].sum(axis=1)
    grouped_data["Numero_piezas"] = grouped_data[columnas_ceramicas].sum(axis=1)
    # Eliminar la columna de código de registro

    return grouped_data


def processnivel(x):
    if isinstance(x, str):
        aux = x.strip('="')
        if aux == "":
            # print('None')
            return None
        # print(aux)
        return int(aux)
    # print(x)
    # Use pd.isna() to check for NaN values in Pandas
    return int(x) if not pd.isna(x) else None


def processestrato(x):
    if isinstance(x, str):
        aux = x.strip('="').replace(",", "").replace(".", "")
        return aux
    return x


# Función para identificar columnas con múltiples tipos de datos
def identify_mixed_type_columns(df):
    mixed_type_columns = []
    for index, col in enumerate(df.columns):
        unique_types = df[col].apply(type).unique()
        # print(f"indice: {index}, Columna: {col}, Tipos Únicos: {unique_types}")
        if len(unique_types) > 1:
            mixed_type_columns.append(col)
    return mixed_type_columns


def remove_unnamed_columns(df):
    unnamed_columns = df.filter(like="Unnamed").columns
    df = df.drop(columns=unnamed_columns)
    return df
