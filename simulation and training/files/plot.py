import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import results
import os

plotter = 5 # 0 per plot reward, 1 per plot energia, 2 per plot energia inferenza, 3 per plot reward-lunghezza episodio, 4 per plot errore posizione, 5 per plot energia media per step


if plotter == 0:
    # Carica il primo file CSV
    dir = results.__path__[0]
    filename1 = dir + '/SAC_inf_5_2_0.csv'
    dataframe1 = pd.read_csv(filename1)

    # Carica il secondo file CSV
    filename2 = dir + '/SAC_e0_5_4_0.csv'  # Modifica con il nome corretto del secondo CSV
    dataframe2 = pd.read_csv(filename2)

    # Funzione per formattare i valori dell'asse x
    def format_func(value, tick_number):
        if value >= 1000:
            return f'{int(value/1000)}k'
        else:
            return int(value)

    # Plotta i dati del primo CSV
    plt.plot(dataframe1['Step'], dataframe1['Value'], label='einf')

    # Plotta i dati del secondo CSV
    plt.plot(dataframe2['Step'], dataframe2['Value'], label='e0')

    # Impostazioni degli assi e titolo
    plt.xlabel('Step',fontweight='bold')
    plt.ylabel('Reward ',fontweight='bold')
    plt.title('Reward medio per Episodio')

    # Applica il formattatore personalizzato all'asse x
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Aggiungi la legenda per identificare le curve
    plt.legend()

    # Mostra la griglia per migliorare la leggibilità
    plt.grid(True)



if plotter == 1:
    # Carica il primo file CSV
    dir = results.__path__[0]
    filename1 = dir + '/train_energy_2.csv'
    dataframe1 = pd.read_csv(filename1)

    # Carica il secondo file CSV
    filename2 = dir + '/train_energy_4.csv'  # Modifica con il nome corretto del secondo CSV
    dataframe2 = pd.read_csv(filename2)

    # Funzione per formattare i valori dell'asse x
    def format_func(value, tick_number):
        if value >= 1000:
            return f'{int(value/1000)}k'
        else:
            return int(value)

    # Plotta i dati del primo CSV
    plt.plot(dataframe1['Step'], dataframe1['Value'], label='einf')

    # Plotta i dati del secondo CSV
    plt.plot(dataframe2['Step'], dataframe2['Value'], label='e0')

    # Impostazioni degli assi e titolo
    plt.xlabel('Episodio',fontweight='bold')
    plt.ylabel('Energia',fontweight='bold')
    plt.title('Energia per episodio (training)')

    # Applica il formattatore personalizzato all'asse x
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Aggiungi la legenda per identificare le curve
    plt.legend()

    # Mostra la griglia per migliorare la leggibilità
    plt.grid(True)


if plotter == 2:
    # Carica il primo file CSV
    dir = results.__path__[0]
    filename1 = dir + '/inference_energy_0.csv'
    dataframe1 = pd.read_csv(filename1)

    # Funzione per formattare i valori dell'asse x
    def format_func(value, tick_number):
        if value >= 1000:
            return f'{int(value/1000)}k'
        else:
            return int(value)

    # Plotta i dati del primo CSV
    plt.plot(dataframe1['Step'], dataframe1['Value'], label='einf')

    # Impostazioni degli assi e titolo
    plt.xlabel('Episodio',fontweight='bold')
    plt.ylabel('Energia',fontweight='bold')
    plt.title('Energia per episodio (inferenza)')

    # Applica il formattatore personalizzato all'asse x
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Aggiungi la legenda per identificare le curve
    plt.legend()

    # Mostra la griglia per migliorare la leggibilità
    plt.grid(True)


if plotter == 3:
    # Carica il primo file CSV
    dir = results.__path__[0]
    filename1 = dir + '/SAC_e0_5_4_0.csv'
    dataframe1 = pd.read_csv(filename1)

    # Carica il secondo file CSV
    filename2 = dir + '/SAC_e0_5_4_0_eplen.csv'  # Modifica con il nome corretto del secondo CSV
    dataframe2 = pd.read_csv(filename2)

    # Funzione per formattare i valori dell'asse x
    def format_func(value, tick_number):
        if value >= 1000:
            return f'{int(value/1000)}k'
        else:
            return int(value)

    fig, ax1 = plt.subplots()

    # Plotta i dati del primo CSV (Reward) sul primo asse y
    ax1.plot(dataframe1['Step'], dataframe1['Value'],color='C1', label='Reward')
    ax1.set_xlabel('Step', fontweight='bold', )
    ax1.set_ylabel('Reward', fontweight='bold')

    # Crea un secondo asse y condividendo lo stesso asse x
    ax2 = ax1.twinx()

    # Plotta i dati del secondo CSV (Lunghezza episodio) sul secondo asse y
    ax2.plot(dataframe2['Step'], dataframe2['Value'],label='Lunghezza Episodio')
    ax2.set_ylabel('Step per episodio', fontweight='bold')
    

    # Applica il formattatore personalizzato all'asse x
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Aggiungi le legende per identificare le curve
    fig.tight_layout()  # Assicura che le etichette non si sovrappongano
    fig.legend(loc='upper left', bbox_to_anchor=(0.15, 0.95))

    # Mostra la griglia per migliorare la leggibilità
    plt.grid(True)

    # Mostra il graficoA
    plt.title('Relazione reward-lunghezza episodio')

if plotter == 4:
    # Carica il primo file CSV
    dir = results.__path__[0]
    filename1 = dir + '/position_error_inf.csv'
    dataframe1 = pd.read_csv(filename1)

    # Carica il secondo file CSV
    filename2 = dir + '/position_error_e0.csv'  # Modifica con il nome corretto del secondo CSV
    dataframe2 = pd.read_csv(filename2)

    # Funzione per formattare i valori dell'asse x
    def format_func(value, tick_number):
        if value >= 1000:
            return f'{int(value/1000)}k'
        else:
            return int(value)

    # Plotta i dati del primo CSV
    plt.plot(dataframe1['Step'], dataframe1['Value'], label='einf')

    # Plotta i dati del secondo CSV
    plt.plot(dataframe2['Step'], dataframe2['Value'], label='e0')

    # Impostazioni degli assi e titolo
    plt.xlabel('Step',fontweight='bold')
    plt.ylabel('|Errore| ',fontweight='bold')
    plt.title('Errore di posizione medio per step')

    # Applica il formattatore personalizzato all'asse x
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Aggiungi la legenda per identificare le curve
    plt.legend()

    # Mostra la griglia per migliorare la leggibilità
    plt.grid(True)

if plotter == 5:
    # Carica il primo file CSV
    dir = results.__path__[0]
    filename1 = dir + '/task_energy_inf.csv'
    dataframe1 = pd.read_csv(filename1)

    # Carica il secondo file CSV
    filename2 = dir + '/task_energy_e0.csv'  # Modifica con il nome corretto del secondo CSV
    dataframe2 = pd.read_csv(filename2)

    # Funzione per formattare i valori dell'asse x
    def format_func(value, tick_number):
        if value >= 1000:
            return f'{int(value/1000)}k'
        else:
            return int(value)

    # Plotta i dati del primo CSV
    plt.plot(dataframe1['Step'], dataframe1['Value'], label='einf')

    # Plotta i dati del secondo CSV
    plt.plot(dataframe2['Step'], dataframe2['Value'], label='e0')

    # Impostazioni degli assi e titolo
    plt.xlabel('Step',fontweight='bold')
    plt.ylabel('Energia ',fontweight='bold')
    plt.title('Energia media per step')

    # Applica il formattatore personalizzato all'asse x
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Aggiungi la legenda per identificare le curve
    plt.legend()

    # Mostra la griglia per migliorare la leggibilità
    plt.grid(True)


# Mostra il grafico
plt.show()
