import pandas as pd

# 1. Folder where you’ve put the Kaggle CSVs
DATA_DIR = "Datasets"

# 2. Load the key files
races        = pd.read_csv(f"{DATA_DIR}/races.csv")
results      = pd.read_csv(f"{DATA_DIR}/results.csv")
drivers      = pd.read_csv(f"{DATA_DIR}/drivers.csv")
constructors = pd.read_csv(f"{DATA_DIR}/constructors.csv")
circuits     = pd.read_csv(f"{DATA_DIR}/circuits.csv")

# 3. Quick checks
print("Races:",    races.shape)
print("Results:",  results.shape)
print("Drivers:",  drivers.shape)
print("Circuits:", circuits.shape)
print(drivers.head())
