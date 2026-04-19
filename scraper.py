import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import os
import time
import fitz

def chercher_arxiv(requete, max_resultats=100):
    requete_encodee = urllib.parse.quote(requete)
    url = f"http://export.arxiv.org/api/query?search_query=all:{requete_encodee}&max_results={max_resultats}&sortBy=relevance"
    req = urllib.request.Request(url, headers={"User-Agent": "MiniRAG/1.0"})
    response = urllib.request.urlopen(req)
    racine = ET.fromstring(response.read())
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    articles = []
    for entree in racine.findall("atom:entry", ns):
        elem_titre = entree.find("atom:title", ns)
        elem_id = entree.find("atom:id", ns)
        if elem_titre is None or elem_id is None:
            continue
        titre = elem_titre.text.strip().replace("\n", " ")
        article_id = elem_id.text.strip().split("/")[-1]
        articles.append({"id": article_id, "titre": titre})
    return articles

def telecharger_et_parser(article_id):
    pdf_url = f"https://arxiv.org/pdf/{article_id}"
    pdf_path = f"/tmp/{article_id.replace('/', '_')}.pdf"
    try:
        req = urllib.request.Request(pdf_url, headers={"User-Agent": "MiniRAG/1.0"})
        with urllib.request.urlopen(req) as response:
            with open(pdf_path, "wb") as f:
                f.write(response.read())
        doc = fitz.open(pdf_path)
        texte = ""
        for page in doc:
            texte += page.get_text()
        doc.close()
        os.remove(pdf_path)
        return texte
    except Exception as e:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        print(f"  erreur {article_id}: {e}")
        return None

def sauvegarder(article_id, titre, texte, dossier="data"):
    os.makedirs(dossier, exist_ok=True)
    nom = article_id.replace(".", "_").replace("/", "_")
    chemin = os.path.join(dossier, f"{nom}.txt")
    with open(chemin, "w") as f:
        f.write(f"{titre}\n\n{texte}")

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

    ids_vus = set()
    total = 0

    for requete in requetes:
        print(f"\nRecherche: {requete}")
        articles = chercher_arxiv(requete, max_resultats=50)
        print(f"  {len(articles)} articles trouves")
        time.sleep(3)

        for article in articles:
            if article["id"] in ids_vus:
                continue
            ids_vus.add(article["id"])

            nom = article["id"].replace(".", "_").replace("/", "_")
            if os.path.exists(f"data/{nom}.txt"):
                total += 1
                continue

            print(f"  telechargement {article['id']}...", end=" ", flush=True)
            texte = telecharger_et_parser(article["id"])
            if texte and len(texte) > 500:
                sauvegarder(article["id"], article["titre"], texte)
                total += 1
                print(f"ok ({len(texte)} chars)")
            else:
                print("trop court, ignore")
            time.sleep(1)

    print(f"\n{total} articles dans data/")
