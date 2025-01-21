import pandas as pd
import matplotlib.pyplot as plt

# Nome del file CSV
csv_file = 'e02.csv'

# Leggi il CSV usando pandas
df = pd.read_csv(csv_file)

# Plotta i dati
plt.plot(df['Step'], df['Position Error (th)'])
plt.xlabel('Step')
plt.ylabel('Position Error (th)')
plt.title('Position Error per Episode')
plt.grid(True)


plt.plot(df['Step'], df['Tank Energy'])
plt.xlabel('Step')
plt.ylabel('Energy')
plt.title('Energia usata')
plt.grid(True)
plt.show()