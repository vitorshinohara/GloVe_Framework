from Features import paper_features

def get_spatial_features(wordarr):
    # Centroid
    for c in paper_features.centroid_location(wordarr):
        yield c
    # Span Volume
    yield paper_features.span_volume(wordarr)
    # Maximum Semantic Span
    yield paper_features.maximun_semantic_span(wordarr)
    # Dispersion Between Semantic Word Embedding Dimensions
    for d in paper_features.dispersion_semantic_word_dimensions(wordarr):
        yield d
