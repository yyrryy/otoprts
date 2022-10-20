from unicodedata import category
import pandas as pd
import os
from models import Produit
#get all files in current directory

files = os.listdir(os.getcwd())
for i, v in enumerate(files):
    print(i, v)
chosen= int(input("Enter the number of the file you want to read: "))
dbframe = pd.read_excel(files[chosen])
print(files[chosen])
for df in dbframe.itertuples():
    print(df.ctg, df.pr)
    Produit.objects.create(category=df.cat)