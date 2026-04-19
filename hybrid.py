def fusionner(scores_bm25, scores_embeddings, k=60):
    rangs_bm25 = sorted(scores_bm25.items(), key=lambda x: x[1], reverse=True)
    rangs_embeddings = sorted(scores_embeddings.items(), key=lambda x: x[1], reverse=True)
    rang_bm25={}
    rang_embeddings={}
    for position, (chunk_id, score) in enumerate(rangs_bm25):
        rang_bm25[chunk_id] = position + 1
    for position, (chunk_id, score) in enumerate(rangs_embeddings):
        rang_embeddings[chunk_id] = position + 1
    scores_rrf = {}
    for chunk_id in rang_bm25:
        scores_rrf[chunk_id] = 1/(k + rang_bm25[chunk_id]) + 1/(k + rang_embeddings[chunk_id])
    return scores_rrf


if __name__ == "__main__":
    scores_bm25 = {0: 2.463, 1: 2.032, 2: 0.208, 3: 0.574, 4: 0.561, 5: 0.209, 6: 0.208, 7: 0.579, 8: 1.047, 9: 1.019}
    scores_emb = {0: 0.335, 1: 0.336, 2: 0.060, 3: 0.072, 4: 0.013, 5: 0.095, 6: 0.280, 7: -0.304, 8: -0.018, 9: 0.413}
    resultats = fusionner(scores_bm25, scores_emb)
    for chunk_id, score in sorted(resultats.items(), key=lambda x: x[1], reverse=True):
        print(f"Chunk {chunk_id}: {score:.6f}")