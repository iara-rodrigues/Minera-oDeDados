import pandas as pd
import re
import spacy

# -----------------------------------------------------------------------------
# ---------------------- Pré processamento do Texto ---------------------------
# -----------------------------------------------------------------------------

# Carregar o modelo de idioma português do spaCy
nlp = spacy.load('pt_core_news_sm')

def normalizar_ementa(ementa):
    ementa = re.sub(r'\bLei\s*n[º°]\s*', 'Lei ', ementa)
    ementa = ementa.replace('§', 'parágrafo')
    ementa = ementa.replace('inc.', 'inciso')
    ementa = ementa.replace('art.', 'artigo')
    return ementa

def tokenizar_ementa(ementa):
    if pd.isna(ementa):  
        return []
    doc = nlp(ementa)
    return [token.text for token in doc]


def stopwords_ementa(ementa):
    if pd.isna(ementa):  
        return []
    doc = nlp(ementa)

    # Adicionando uma stopword personalizada
    nlp.vocab['('].is_stop = True
    nlp.vocab[')'].is_stop = True
    nlp.vocab['.'].is_stop = True
    nlp.vocab[','].is_stop = True
    nlp.vocab[';'].is_stop = True
    nlp.vocab['!'].is_stop = True
    nlp.vocab['?'].is_stop = True

    tokens_sem_stopwords = [token.text for token in doc if not token.is_stop]
    return tokens_sem_stopwords

def lematizar_ementa(ementa):
    if pd.isna(ementa): 
        return []
    doc = nlp(ementa)
    # doc = tokenizar_ementa
    lemas = [token.lemma_ for token in doc if not token.is_stop]  
    return lemas

df = pd.read_csv('pl_atualizado.csv')

df['Ementa Normalizada'] = df['Ementa'].apply(normalizar_ementa)

df.to_csv('pl_normalizado.csv', index=False)
print("Arquivo normalizado salvo como 'pl_normalizado.csv'")

df = pd.read_csv('pl_normalizado.csv')

df['Ementa Tokenizada'] = df['Ementa Normalizada'].apply(tokenizar_ementa)
df['Ementa Sem Stopwords'] = df['Ementa Normalizada'].apply(stopwords_ementa)
df['Ementa Lematizada'] = df['Ementa Normalizada'].apply(lematizar_ementa)

df.to_csv('tecnicas.csv', index=False)

print("Arquivo completo com técnicas salvo como 'tecnicas.csv'")