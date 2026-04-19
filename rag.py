from tokeniser import tokeniser
from chunker import decouper
from bm25 import construire_index, calculer_idf, scorer_bm25
from embeddings import vecteur_moyen, chercher
from hybrid import fusionner
from textrank import decouper_phrase, text_rank

texte = open("data/Solar_panel.txt").read()
mots = tokeniser(texte)
chunks = decouper(mots)

index = construire_index(chunks)
idf = calculer_idf(index, len(chunks))

def poserquestion(question, chunks, index, idf):
    score_bm25 = scorer_bm25(tokeniser(question), chunks, index, idf)
    score_embeddings =  chercher(question, chunks)
    hybride = fusionner(score_bm25, score_embeddings)
    hybride = sorted(hybride.items(), key=lambda x: x[1], reverse=True)
    top_ids = [chunk_id for chunk_id, score in hybride[:3]]
    texte_top = " ".join([" ".join(chunks[i]) for i in top_ids])
    phrases = decouper_phrase(texte_top)
    reponse = text_rank(phrases)
    return reponse

if __name__ == "__main__":
    reponse = poserquestion("how do solar panels generate electricity", chunks, index, idf)
    for phrase, score in reponse:
        print(f"[{score:.4f}] {phrase[:100]}")

