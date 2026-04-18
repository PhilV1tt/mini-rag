def decouper(mots, taille=512, overlap=100):
    chunks=[]
    pas = taille-overlap
    for i in range(0, len(mots), pas):
        chunk = mots[i:i+taille]
        chunks.append(chunk)
    return chunks        