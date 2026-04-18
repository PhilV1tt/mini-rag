import re
STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for", "of", "and", "or", "but", "not", "with", "by", "from", "this", "that", "it", "as", "be", "has", "have", "had", "do", "does", "did", "will", "would", "can", "could", "should", "may", "might", "its", "their", "they", "he",
  "she", "we", "you", "i", "my", "your", "his", "her", "our", "no", "if", "then", "than", "so", "very", "just", "about", "also", "been", "being", "each", "which", "when", "where", "how", "all", "any", "both", "few", "more", "most", "other", "some", "such", "into", "over", "after", "before", "between", "under",
  "again", "there", "here", "up", "out", "off", "down", "only", "own", "same", "too", "s", "t"}
def tokeniser(texte):
    mots=re.findall(r'\w+', texte.lower())
    mots = [mot for mot in mots if mot not in STOPWORDS]
    return mots

print(tokeniser("The Solar panel costs $500!"))