#Aqui é basico mas vou deixar comentado pra que todos entendam
import pandas as pd

#leio o dataset original que ta nessa pasta
df = pd.read_csv("data/airlines_flights_data.csv")

#filtro pegando so a SpiceJet
df_spiceJet = df[df["airline"] == "SpiceJet"]

#crio outro dataset e envio ele pra a pasta de data
df_spiceJet.to_csv("data/airlines_spicejet.csv", index = False)

#teste para ver se realemnte foi criado
print("Arquivo criado")