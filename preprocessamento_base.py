import pandas as pd

# -----------------------------------------------------------------------------
# ----------------------- Pré processamento da Base ---------------------------
# -----------------------------------------------------------------------------

df = pd.read_csv('projetos_lei.csv')
print(df.head())

df['Autor Nome'] = df['Autor'].apply(lambda x: x.replace("Autor: ", "").split(" - ")[0] if " - " in x else "")
df['Partido'] = df['Autor'].apply(lambda x: x.split(" - ")[1].split("/")[0] if " - " in x and "/" in x else "")
df['Estado'] = df['Autor'].apply(lambda x: x.split("/")[-1] if "/" in x else "")

df['Número da PL'] = df['Número da PL'].apply(lambda x: x.replace("PL ", "") if "PL " in x else x)

df['Data'] = df['Data'].apply(lambda x: x.split()[1] if len(x.split()) > 1 else x)

def ajustar_ementa(texto):
    if pd.isna(texto):  
        return texto
    texto = texto.replace('"', '').replace("''", "").replace('”', '').replace('“', '')
    texto = texto.replace('Ementa:', '').replace('"Ementa:', '')
    texto = texto.strip()
    return texto

df['Ementa'] = df['Ementa'].apply(ajustar_ementa)

df = df.drop(columns=['Autor'])

df = df[['Número da PL', 'Autor Nome', 'Partido', 'Estado', 'Ementa', 'Data']]

df.to_csv('pl_atualizado.csv', index=False)

print("Arquivo atualizado salvo como 'pl_atualizado.csv'")