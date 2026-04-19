import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import os
import time

def chercher_arxiv(requete, max_resultats=100):
    requete_encodee = urllib.parse.quote(requete)
    url = f"http://export.arxiv.org/api/query?search_query=all:{requete_encodee}&max_results={max_resultats}&sortBy=relevance"
    req = urllib.request.Request(url, headers={"User-Agent": "MiniRAG/1.0"})
    response = urllib.request.urlopen(req)
    xml_brut = response.read()
    racine = ET.fromstring(xml_brut)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    articles = []
    for entree in racine.findall("atom:entry", ns):
        titre = entree.find("atom:title", ns).text.strip().replace("\n", " ")
        resume = entree.find("atom:summary", ns).text.strip().replace("\n", " ")
        article_id = entree.find("atom:id", ns).text.strip().split("/")[-1]
        articles.append({"id": article_id, "titre": titre, "resume": resume})
    return articles

def sauvegarder(articles, dossier="data"):
    os.makedirs(dossier, exist_ok=True)
    for article in articles:
        nom_fichier = article["id"].replace(".", "_").replace("/", "_")
        chemin = os.path.join(dossier, f"{nom_fichier}.txt")
        contenu = f"{article['titre']}\n\n{article['resume']}"
        fichier = open(chemin, "w")
        fichier.write(contenu)
        fichier.close()

if __name__ == "__main__":
    requetes = [
        "model compression pruning quantization",
        "knowledge distillation neural network",
        "pruning deep neural networks",
        "quantization aware training",
        "neural network optimization efficiency",
        "model compression survey",
        "sparse neural networks",
        "low rank approximation neural",
        "efficient inference deep learning",
        "mixed precision training",
    ]
    tous_les_articles = []
    for requete in requetes:
        print(f"Recherche: {requete}")
        articles = chercher_arxiv(requete, max_resultats=50)
        tous_les_articles.extend(articles)
        print(f"  -> {len(articles)} articles trouves")
        time.sleep(3)

    ids_vus = set()
    articles_uniques = []
    for article in tous_les_articles:
        if article["id"] not in ids_vus:
            ids_vus.add(article["id"])
            articles_uniques.append(article)

    sauvegarder(articles_uniques)
    print(f"\n{len(articles_uniques)} articles uniques sauvegardes dans data/")
