import pandas as pd
import pyxdameraulevenshtein as dl
import re

# Load npi_with_dob.csv and pecos_with_dob.csv
npi = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

print("NPI Data:")
print(npi.iloc[13])

print("PECOS Data for index 2968:")
print(pecos_with_dob.iloc[2968])

print("\nPECOS Data for index 1480:")
print(pecos_with_dob.iloc[1480])
