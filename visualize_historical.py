# visualize_historical.py
import pandas as pd
import matplotlib.pyplot as plt
from config import PROCESSED_CSV

# ------------------------------
# 1. Load Data
# ------------------------------
df = pd.read_csv(PROCESSED_CSV)
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

# ------------------------------
# 2. Plot Function
# ------------------------------
def plot_and_save(column, ylabel, filename):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df[column], color='tab:blue', lw=1)
    plt.title(f'{column} over Time')
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'data/plots/{filename}')  # saves file in data/plots/
    plt.close()  # prevents display issues

# ------------------------------
# 3. Make sure folder exists
# ------------------------------
import os
os.makedirs('data/plots', exist_ok=True)

# ------------------------------
# 4. Plot all parameters
# ------------------------------
plot_and_save('temp', 'Temperature (°C)', 'temp.png')
plot_and_save('rhum', 'Relative Humidity (%)', 'rhum.png')
plot_and_save('prcp', 'Precipitation (mm)', 'prcp.png')
plot_and_save('wspd', 'Wind Speed (km/h)', 'wspd.png')
plot_and_save('pres', 'Pressure (hPa)', 'pres.png')

print("✅ All historical plots saved in data/plots/")
