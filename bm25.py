from tokeniser import tokeniser
from chunker import decouper
import math

texte = open("data/Solar_panel.txt").read()
mots = tokeniser(texte)
chunks = decouper(mots)

def construire_index(chunks):
    index = {}
    for i, chunk in enumerate(chunks):
        for mot in chunk:
            if mot not in index:
                index[mot]={}
            if i not in index[mot]:
                index[mot][i] = 0
            index[mot][i] += 1
    return index

def calculer_idf(index, nb_chunks):
    idf = {}
    for mot in index:
        n = len(index[mot])
        idf[mot]=math.log((nb_chunks-n+0.5)/(n+0.5)+1)
    return idf

def scorer_bm25(question, chunks, index, idf, k1=1.5, b=0.75):
    avgdl = sum(len(c) for c in chunks)/len(chunks)
    scores = {}
    for i, chunk in enumerate(chunks):
        score = 0
        for mot in question:
            if mot not in idf:
                continue
            if mot in index and i in index[mot]:
                f = index[mot][i]
            else:
                f=0
            score += idf[mot] * (f * (k1 + 1)) / (f + k1 * (1 - b + b * len(chunks[i]) / avgdl))
        scores[i]=score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        

index = construire_index(chunks)
idf = calculer_idf(index, len(chunks))
question = tokeniser("how do solar panels generate electricity")
scores = scorer_bm25(question, chunks, index, idf)
print(scores)