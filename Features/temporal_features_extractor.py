from Features import paper_features

def get_temporal_features(wordarr):
    out = []
    # Average Step Size
    out.append(paper_features.avg_step_size(wordarr))
    # Variation Step Size
    for vss in paper_features.variation_step_size(wordarr):
        out.append(vss)
    # Average Adjacent Edge Angles
    out.append(paper_features.avg_adjacent_edge_angles(wordarr))
    # Mean of Adjacent Edge Angle Increment
    out.append(paper_features.mean_adjacent_edge_angle_increment(wordarr))
    return out
