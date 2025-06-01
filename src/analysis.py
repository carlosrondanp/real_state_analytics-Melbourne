def analyze_outliers_mixed_data(df, numerical_cols, categorical_cols, contamination=0.05, plot=True):
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import IsolationForest
    from prince import FAMD
    import matplotlib.pyplot as plt
  
    # Copiar datos originales
    data = df[numerical_cols + categorical_cols].copy()

    scaler = StandardScaler()
    data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

    # Preparar los datos combinados
    data_encoded = data[numerical_cols + categorical_cols]

    # Aplicar FAMD (Factor Analysis of Mixed Data)
    famd = FAMD(n_components=2, random_state=42)
    famd_result = famd.fit_transform(data_encoded)

    # Isolation Forest para detectar outliers
    iso_forest = IsolationForest(
        contamination=contamination,
        n_estimators=100,
        max_samples=0.5,
        max_features=0.8,
        random_state=42
    )
    data['Outlier'] = iso_forest.fit_predict(famd_result)

    # Crear gráficos
    if plot:
        plt.figure(figsize=(10, 6))
        plt.scatter(famd_result.iloc[:, 0], famd_result.iloc[:, 1], c=data['Outlier'], cmap='bwr', s=20)
        plt.title('Proyección FAMD: Detección de Outliers con Isolation Forest')
        plt.xlabel('FAMD Componente 1')
        plt.ylabel('FAMD Componente 2')
        plt.colorbar(label='Outlier (-1: Sí, 1: No)')
        plt.show()

    # Filtrar outliers
    cleaned_data = df[data['Outlier'] == 1]

    print(f"Outliers detectados y eliminados: {len(df) - len(cleaned_data)}")
    return cleaned_data, scaler, famd, iso_forest


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats

def analisis_variables_numericas_continuo(data, target):
    resumen = {'variable': [], 'normal': [], 'p_value': [], 'correlacion_pearson': []}

    if target not in data.columns:
        raise ValueError("El target debe estar incluido en el DataFrame.")

    # Seleccionar variables numéricas excepto el target
    data_ = data.select_dtypes(include=np.number).drop(columns=[target]).copy()
    variables = data_.columns
    filas = len(variables)
    columnas = 4

    fig, axs = plt.subplots(filas, columnas, figsize=(18, 3.5 * filas), constrained_layout=True)
    fig.suptitle(f'Análisis de variables numéricas vs target continuo ({target})',
                 fontsize=20, ha='left', x=0.01, y=1.02)

    axs = np.atleast_2d(axs)

    for fila, col in enumerate(variables):
        try:
            data_no_null = data[[col, target]].dropna()

            # Histograma + KDE
            sns.histplot(data=data_no_null, x=col, stat='density', color='gray',
                         bins=30, edgecolor="gray", alpha=0.2, ax=axs[fila][0])
            sns.kdeplot(data=data_no_null, x=col, color='#1C60A5', ax=axs[fila][0])
            normal = pd.DataFrame({'valor': np.random.normal(
                data_no_null[col].mean(), data_no_null[col].std(), size=100000)})
            sns.kdeplot(data=normal, x='valor', color='salmon', ax=axs[fila][0])
            axs[fila][0].axvline(data_no_null[col].mean(), linestyle='--', color='red', label='media')
            axs[fila][0].axvline(data_no_null[col].median(), linestyle='--', color='green', label='mediana')
            axs[fila][0].legend()
            axs[fila][0].set_title(f'Distribución de {col}')
            axs[fila][0].grid(True)

            # Boxplot
            sns.boxplot(y=data_no_null[col], ax=axs[fila][1], color='gray')
            axs[fila][1].set_title(f'Boxplot de {col}')
            axs[fila][1].grid(True)

            # QQplot
            pg.qqplot(data_no_null[col], dist='norm', ax=axs[fila][2])
            axs[fila][2].set_title(f'QQplot de {col}')
            axs[fila][2].grid(True)

            # Scatter + regresión lineal
            sns.regplot(x=col, y=target, data=data_no_null, ax=axs[fila][3],
                        line_kws={"color": "red"}, scatter_kws={"alpha": 0.5})
            axs[fila][3].set_title(f'{col} vs {target}')
            axs[fila][3].grid(True)

            # Estadísticas
            k2, p_value = stats.normaltest(data_no_null[col])
            corr = data_no_null[[col, target]].corr(method='pearson').iloc[0, 1]

            resumen['variable'].append(col)
            resumen['normal'].append('Sí' if p_value > 0.05 else 'No')
            resumen['p_value'].append(p_value)
            resumen['correlacion_pearson'].append(corr)

        except Exception as e:
            print(f'Error con la variable {col}: {e}')
            continue

    plt.show()
    display(pd.DataFrame(resumen))




import json
def winsorize_dataframe(df, numerical_cols, lower_pct=0.01, upper_pct=0.995, save_path=None):
    """
    Aplica winsorización a columnas numéricas y opcionalmente guarda los cortes en un JSON.

    Parámetros:
    - df: DataFrame original
    - numerical_cols: lista de columnas numéricas
    - lower_pct: percentil inferior (por defecto 1%)
    - upper_pct: percentil superior (por defecto 99%)
    - save_path: ruta del archivo .json para guardar los cortes (opcional)

    Retorna:
    - df_winsorized: DataFrame con winsorización aplicada
    - cutoffs: diccionario con percentiles por columna
    """
    df_winsorized = df.copy()
    cutoffs = {}

    for col in numerical_cols:
        lower = df[col].quantile(lower_pct)
        upper = df[col].quantile(upper_pct)
        cutoffs[col] = {'lower': lower, 'upper': upper}
        df_winsorized[col] = df[col].clip(lower=lower, upper=upper)

    if save_path:
        with open(save_path, 'w') as f:
            json.dump(cutoffs, f, indent=4)
        print(f"Cortes guardados en: {save_path}")

    return df_winsorized, cutoffs


def apply_winsorization_from_json(df, numerical_cols, json_path):
    """
    Aplica winsorización a un nuevo DataFrame usando cortes guardados en un archivo JSON.

    Parámetros:
    - df: DataFrame a transformar
    - numerical_cols: columnas numéricas a winsorizar
    - json_path: ruta del archivo JSON con los cortes guardados

    Retorna:
    - df_winsorized: DataFrame con winsorización aplicada
    """
    # Cargar los cortes desde el archivo JSON
    with open(json_path, 'r') as f:
        cutoffs = json.load(f)

    df_winsorized = df.copy()

    for col in numerical_cols:
        if col in cutoffs:
            lower = cutoffs[col]['lower']
            upper = cutoffs[col]['upper']
            df_winsorized[col] = df[col].clip(lower=lower, upper=upper)
        else:
            print(f"Advertencia: La columna '{col}' no está en el archivo de cortes.")

    return df_winsorized