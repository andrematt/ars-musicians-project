import pandas as pd


a = pd.read_csv("data/network_new.csv", low_memory=False, delimiter="\t")
b = pd.read_csv("data/semantictsv.csv", delimiter="\t")


merged = a.merge(b, on='personLabel')

merged.to_csv("merge_new.csv", index=False)