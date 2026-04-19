from wordtovec import mot_vers_id, id_vers_mot, taille_vocab, dim_embedding
from tokeniser import tokeniser
from chunker import decouper
import torch.nn as nn
import torch

embedding = nn.Embedding(taille_vocab, dim_embedding)
embedding.load_state_dict(torch.load("vecteurs.pt"))


def vecteur_moyen(mots):
    vecteurs = []
    for mot in mots:
        if mot not in mot_vers_id:
            continue
        vecteurs.append(embedding(torch.tensor(mot_vers_id[mot])))
    return torch.stack(vecteurs).mean(dim=0)


def chercher(question, chunks):
    vec_question = vecteur_moyen(tokeniser(question))
    cos = nn.CosineSimilarity(dim=0)
    scores_embeddings = {}
    for i,chunk in enumerate(chunks):
        scores_embeddings[i] = cos(vec_question,vecteur_moyen(chunk)).item()
    return scores_embeddings
        



texte = open("data/Solar_panel.txt").read()
mots = tokeniser(texte)
chunks = decouper(mots)
resultats = chercher("how do solar panels work", chunks)
print(resultats)