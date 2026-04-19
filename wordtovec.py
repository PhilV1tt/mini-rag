import torch, os
import torch.nn as nn
from tokeniser import tokeniser

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Device: {device}")

texte = ""
for fichier in os.listdir("data"):
    texte += open(f"data/{fichier}").read() + " "

mots = tokeniser(texte)
mots = mots[:500000]
mots_uniques=list(set(mots))
taille_vocab = len(mots_uniques)
dim_embedding = 128

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
    vec = embedding_central(torch.tensor(mot_vers_id[mot]).to(device))
    scores = {}
    for autre_mot, autre_id in mot_vers_id.items():
        if autre_mot == mot:
            continue
        autre_vec = embedding_central(torch.tensor(autre_id).to(device))
        cos = nn.functional.cosine_similarity(vec.unsqueeze(0), autre_vec.unsqueeze(0))
        scores[autre_mot] = cos.item()
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]


if __name__=="__main__":
    embedding_central = nn.Embedding(taille_vocab, dim_embedding).to(device)
    embedding_contexte = nn.Embedding(taille_vocab, dim_embedding).to(device)
    descente = torch.optim.SGD(list(embedding_central.parameters())+list(embedding_contexte.parameters()),lr=0.025)
    print(f"{len(mots)} mots, {len(mots_uniques)} uniques")
    paires = creer_paires(mots)
    
    centraux = torch.tensor([p[0] for p in paires]).to(device)
    contextes = torch.tensor([p[1] for p in paires]).to(device)
    batch_size = 1024
    for epoch in range(100):
        total_loss=0
        for i in range(0, len(paires), batch_size):
            descente.zero_grad()
            batch_c = centraux[i:i+batch_size]
            batch_ctx = contextes[i:i+batch_size]
            vec_c = embedding_central(batch_c)
            vec_ctx = embedding_contexte(batch_ctx)

            produit = (vec_c * vec_ctx).sum(dim=1)
            loss_pos = -torch.log(torch.sigmoid(produit)).mean()
            

            negatifs = torch.randint(0, taille_vocab, (len(batch_c), 5)).to(device) 
            vec_neg = embedding_contexte(negatifs) 
            produit_neg = (vec_c.unsqueeze(1) * vec_neg).sum(dim=2) 
            loss_neg = -torch.log(torch.sigmoid(-produit_neg)).mean()

            loss = loss_pos + loss_neg
            loss.backward()
            descente.step()
            
            total_loss += loss.item()
        nb_batches = len(paires) // batch_size
        print(f"Epoch {epoch}, fonction perte moyenne: {total_loss/nb_batches:.4f}")

    torch.save(embedding_central.state_dict(), "vecteurs.pt")
    print(mots_proches("pruning"))