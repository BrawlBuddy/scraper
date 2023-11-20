import pickle

with open("entries.pickle", "rb") as f:
    entries = pickle.load(f)

print(entries)