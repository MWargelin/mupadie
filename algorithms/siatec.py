from collections import defaultdict

def compute(point_set, min_pattern_length=2):
    point_set = sorted(point_set)
    mtps = _maximal_translatable_patterns(point_set, min_length=min_pattern_length)
    vector_table = _vector_table(point_set)
    translation_vectors = _translation_vectors(mtps, vector_table)
    result = _format_for_visualisation(translation_vectors)
    return result


def _vector_table(point_set):
    return {a:[ (b[0]-a[0], b[1]-a[1]) for b in point_set ] for a in point_set}


def _maximal_translatable_patterns(point_set, min_length=0):
    mtps = defaultdict(list)
    for i in range(len(point_set)):
        for j in range(i+1, len(point_set)):
            vector = (point_set[j][0]-point_set[i][0], point_set[j][1]-point_set[i][1])
            mtps[vector].append(point_set[i])

    mtps = {k:v for k, v in mtps.items() if len(v) >= min_length}
    mtps = {key:sorted(mtp) for key, mtp in mtps.items()}
    mtps = {k:mtps[k] for k in sorted(mtps.keys())}
    return mtps


def _translation_vectors(mtps, vector_table):
    translation_vectors = []
    for mtp in mtps.values():
        intersection = set(vector_table[mtp[0]])
        for point in mtp:
            intersection.intersection_update(set(vector_table[point]))
        translation_vectors.append({'pattern': mtp, 'translation_vectors': sorted(intersection)})
    return translation_vectors


def _get_instances(pattern, translation_vectors):
    instances = []
    for vector in translation_vectors:
        instances.append([(point[0] + vector[0], point[1] + vector[1]) for point in pattern])
    return instances


def _format_for_visualisation(translation_vectors):
    translation_vectors = sorted(translation_vectors,
                                 key=lambda pattern: len(pattern['pattern']),
                                 reverse=True)
    patterns = []
    for pattern in translation_vectors:
        patterns.append(_get_instances(pattern['pattern'], pattern['translation_vectors']))
    return patterns
