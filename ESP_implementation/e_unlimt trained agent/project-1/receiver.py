


import serial
import csv

# Configurazione della porta seriale
ser = serial.Serial('COM6', 115200)
ser.flushInput()
csv_file = 'inference_data.csv'



# Funzione per acquisire dati via UART e salvarli su CSV
def acquire_and_save_data():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Scrivi l'intestazione
        writer.writerow(['Episode', 'Step','Position Error (th)', 'Velocity', 'Tank Energy'])

        while True:
            try:
                # Leggi una riga dalla porta seriale
                line = ser.readline().decode('utf-8').strip()
                print(line)  # Per vedere il dato ricevuto
                values =  line.split(',')
                if len(values) == 5:  # Assicurati di ricevere due valori
                    writer.writerow([values[0],values[1], values[2], values[3],values[4]])

            except KeyboardInterrupt:
                print("Acquisizione interrotta.")
                break

# Avvia l'acquisizione
if __name__ == '__main__':
    acquire_and_save_data()
