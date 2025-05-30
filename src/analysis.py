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