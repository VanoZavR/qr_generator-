import pandas as pd


novy_excel = "novy_excel.xlsx"

df = pd.read_excel(novy_excel, header=None, dtype=str)

pervyi_stolbec = df.iloc[:, 0]

gotovaya_ssylka = []

for y in pervyi_stolbec:
    ssylka = "https://app.skurtt.me/" + str(y)
    gotovaya_ssylka.append(ssylka)

df[1] = gotovaya_ssylka

df.to_excel("data.xlsx", index=False, header=False)