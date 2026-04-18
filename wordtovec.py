import torch
import torch.nn as nn
from tokeniser import tokeniser

texte=open("data/Solar_panel.txt").read()
mots = tokeniser(texte)
mots_uniques=list(set(mots))
taille_vocab = len(mots_uniques)
dim_embedding = 16

mot_vers_id = {}
for i, mot in enumerate(mots_uniques):
    mot_vers_id[mot]=i

id_vers_mot = {}
for i, mot in enumerate(mots_uniques):
    id_vers_mot[i]=mot

def creer_paires(mots, fenetre=2):
    paires=[]
    for i in range(len(mots)):
        mot_central = mot_vers_id[mots[i]]
        for j in range(max(0, i-fenetre), min(len(mots), i+fenetre+1)):
            if j != i:
                paires.append((mot_central, mot_vers_id[mots[j]]))
    return paires

def mots_proches(mot, top_k=5):
    vec = embedding_central(torch.tensor(mot_vers_id[mot]))
    scores = {}
    for autre_mot, autre_id in mot_vers_id.items():
        if autre_mot == mot:
            continue
        autre_vec = embedding_central(torch.tensor(autre_id))
        score = torch.dot(vec, autre_vec).item()
        scores[autre_mot] = score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]


embedding_central = nn.Embedding(taille_vocab, dim_embedding)
embedding_contexte = nn.Embedding(taille_vocab, dim_embedding)

descente = torch.optim.SGD(list(embedding_central.parameters())+list(embedding_contexte.parameters()),lr=0.001)
paires = creer_paires(mots)
for epoch in range(10):
    total_loss=0
    for idx, paire in enumerate(paires):
        negative_sampling = 0
        descente.zero_grad()
        id_central = paire[0]
        id_contexte = paire[1]
        vec_central = embedding_central(torch.tensor(id_central))
        vec_contexte = embedding_contexte(torch.tensor(id_contexte))
        mots_negatifs = torch.randint(0, taille_vocab, (5,))
        for mot_negatif in mots_negatifs:
            vec_negatif = embedding_contexte(mot_negatif)
            negative_sampling += -torch.log(torch.sigmoid(-torch.dot(vec_central,vec_negatif)))
        produit = torch.dot(vec_central,vec_contexte)
        loss = -torch.log(torch.sigmoid(produit)) + negative_sampling
        loss.backward()
        descente.step()
        if idx % 3000 == 0:
            print(f"Paire {idx}/{len(paires)}, loss: {loss.item():.4f}")
        total_loss += loss.item()
    print(f"Epoch {epoch}, loss moyenne: {total_loss/len(paires):.4f}")


print(mots_proches("solar"))
