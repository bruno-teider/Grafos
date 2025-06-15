def normalize_betweenness_centrality(resultado_centralidades, n_vertices, is_directed=False):
    if n_vertices <= 2:
        return {v: 0.0 for v in resultado_centralidades}
    normalization_factor = (n_vertices - 1) * (n_vertices - 2) / 2.0
    normalized_results = {}
    for vertice in resultado_centralidades:
        normalized_results[vertice] = resultado_centralidades[vertice] / normalization_factor
    
    return normalized_results

# Example usage with your data
raw_centralities = {
    'ANUPAM KHER': 75733891.7677,
    'OM PURI': 27605614.5028,
    'SAHAJAK BOONTHANAKIT': 24915084.6020,
    'MICHAEL MADSEN': 24713222.3581,
    'BEN KINGSLEY': 23007026.1294,
    'CHRISTOPHER LEE': 22552984.4478,
    'IKO UWAIS': 21586227.7687,
    'STEVEN YEUN': 18025061.2934,
    'DEAN CAIN': 17386274.2139,
    'PRIYANKA CHOPRA': 16738274.7810
}

n_vertices = 60922 

normalized_centralities = normalize_betweenness_centrality(
    raw_centralities, 
    n_vertices, 
    is_directed=False 
)

print("Maiores Intermediacoes: ")
for actor, centrality in normalized_centralities.items():
    print(f"{actor}: {centrality:.6f}")