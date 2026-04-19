import numpy as np
def decouper_phrase(texte):
    phrases = texte.split(".")
    phrases = [p.strip() for p in phrases if p.strip()]
    return phrases

def text_rank(phrases, top_k=3):
    N = len(phrases)
    matrice = np.zeros((N,N))
    for i in range(N):
        mots_i = set(phrases[i].lower().split())
        for j in range(N):
            mots_j = set(phrases[j].lower().split())
            if i!=j:
                communs = mots_i & mots_j
                total = mots_i | mots_j
                jaccard = len(communs)/len(total)
                matrice[i][j] = jaccard
    for j in range(N):
        somme = matrice[:, j].sum()
        if somme>0:
            matrice[:,j] /= somme
    scores = np.ones(N) / N
    damping=0.85
    for _ in range(50):
        scores = damping * matrice @ scores + (1 - damping) / N
    top_indices = scores.argsort()[::-1][:top_k]
    return [(phrases[i],scores[i]) for i in top_indices]

if __name__ == "__main__":
    texte = open("data/Solar_panel.txt").read()
    phrases = decouper_phrase(texte)
    resultats = text_rank(phrases)
    for phrase, score in resultats:
        print(f"[{score:.4f}] {phrase[:80]}...")

