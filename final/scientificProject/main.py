import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("boli_simptome.csv")

romanian_stopwords = [
    "în", "și", "sau", "la", "cu", "pe", "ca", "de", "din", "un", "o", "este",
    "sunt", "fi", "fie", "a", "al", "ai", "ale", "într", "ce", "care", "cum",
    "dacă", "nu", "da", "pentru", "lui", "ei", "el", "ea", "acest", "această",
    "aceste", "acela", "acelea", "acei", "acestora", "acelui", "acelei", "le",
    "li", "lor", "să", "se", "ne", "vă", "te", "mi", "ți", "mai", "foarte"
]

vectorizer = TfidfVectorizer(stop_words=romanian_stopwords)

# 3. Transformăm simptomele în matrice BoW (Bag-of-Words)
X = vectorizer.fit_transform(df["simptome"])


# 4. Funcție pentru a face predicția
def identifica_boala(simptome_user):
    simptome_user = [simptome_user.lower()]  # Normalizare la lowercase
    vector_user = vectorizer.transform(simptome_user)  # Transformăm input-ul
    similaritati = cosine_similarity(vector_user, X)  # Calculăm similaritatea cosine

    # Identificăm boala cu cea mai mare similaritate
    idx = similaritati.argmax()
    boala_probabila = df.iloc[idx]["nume_boala"]

    return boala_probabila, similaritati[0][idx]


# 5. Extragere simptome de la utilizator
simptome_input = input("Introdu simptomele (separate prin virgulă): ")
boala, scor = identifica_boala(simptome_input)

# 6. Afișăm rezultatul
print(f"\n🔎 Cea mai probabilă boală: {boala}")
print(f"📊 Scor de similaritate: {scor:.2f}")

