import urllib.request
import urllib.parse
import json
def fetch_article(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles={title}&explaintext=1&format=json"
    req = urllib.request.Request(url, headers={"User-Agent" : "mini-rag",})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    #fichier_test = open("temp.json","w")
    #fichier_test.write(json.dumps(data, indent=2))
    #fichier_test.close()
    page = list(data["query"]["pages"].values())[0]
    extrait = page["extract"]
    return extrait 

if __name__ == "__main__":
    titles = ["Solar", "Solar_panel","Solar_energy","Photovoltaics"]
    for title in titles:
        article = open(f"data/{title}.txt", "w")
        article.write(fetch_article(title))
        article.close()

