import pandas as pd

old_excel = "sozdanie_qr.xlsx"

chit = pd.read_excel(old_excel, header=None)

last_symbols = []

for i in chit[0]:
    ssylka = str(i)
    nomer = ssylka[-6:]
    last_symbols.append(nomer)

df = pd.DataFrame(last_symbols)

df.to_excel("novy_excel.xlsx", index=False, header=False)



novy_excel = "novy_excel.xlsx"

df = pd.read_excel(novy_excel, header=None)

pervyi_stolbec = df.iloc[:, 0]

gotovaya_ssylka = []

for y in pervyi_stolbec:
    ssylka = "https://app.skurtt.me/" + str(y)
    gotovaya_ssylka.append(ssylka)

df[1] = gotovaya_ssylka

df.to_excel("data.xlsx", index=False, header=False)

