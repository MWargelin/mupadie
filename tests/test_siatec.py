from algorithms import siatec


def test_vector_table(sorted_point_set):
    result = siatec._vector_table(sorted_point_set)
    assert result == {
        (1,1): [(0,0), (0,2), (1,0), (1,1), (1,2), (2,1)],
        (1,3): [(0,-2), (0,0), (1,-2), (1,-1), (1,0), (2,-1)],
        (2,1): [(-1,0), (-1,2), (0,0), (0,1), (0,2), (1,1)],
        (2,2): [(-1,-1), (-1,1), (0,-1), (0,0), (0,1), (1,0)],
        (2,3): [(-1,-2), (-1,0), (0,-2), (0,-1), (0,0), (1,-1)],
        (3,2): [(-2,-1), (-2,1), (-1,-1), (-1,0), (-1,1), (0,0)]
    }


def test_maximal_translatable_patterns(sorted_point_set):
    result = siatec._maximal_translatable_patterns(sorted_point_set, min_length=2)
    assert result == {
        (0,1): [(2,1), (2,2)],
        (0,2): [(1,1), (2,1)],
        (1,-1): [(1,3), (2,3)],
        (1,0): [(1,1), (1,3), (2,2)],
        (1,1): [(1,1), (2,1)]
    }


def test_translation_vectors(sorted_point_set):
    mtps = siatec._maximal_translatable_patterns(sorted_point_set)
    vector_table = siatec._vector_table(sorted_point_set)
    translation_vectors = siatec._translation_vectors(mtps, vector_table)
    assert translation_vectors == [
        {'pattern': [(2,1), (2,2)], 'translation_vectors': [(0,0), (0,1)]},
        {'pattern': [(1,1), (2,1)], 'translation_vectors': [(0,0), (0,2), (1,1)]},
        {'pattern': [(1,3)], 'translation_vectors': [(0,-2), (0,0), (1,-2), (1,-1), (1,0), (2,-1)]},
        {'pattern': [(1,3), (2,3)], 'translation_vectors': [(0,-2), (0,0), (1,-1)]},
        {'pattern': [(1,1), (1,3), (2,2)], 'translation_vectors': [(0,0), (1,0)]},
        {'pattern': [(1,1), (2,1)], 'translation_vectors': [(0,0), (0,2), (1,1)]},
        {'pattern': [(1,1)], 'translation_vectors': [(0,0), (0,2), (1,0), (1,1), (1,2), (2,1)]},
        {'pattern': [(1,3)], 'translation_vectors': [(0,-2), (0,0), (1,-2), (1,-1), (1,0), (2,-1)]},
        {'pattern': [(1,1)], 'translation_vectors': [(0,0), (0,2), (1,0), (1,1), (1,2), (2,1)]}
    ]


def test_get_instances():
    pattern = {'pattern': [(1,1), (1,3), (2,2)], 'translation_vectors': [(0,0), (1,-1)]}
    instances = siatec._get_instances(pattern['pattern'], pattern['translation_vectors'])
    assert instances == [
        [(1,1), (1,3), (2,2)],
        [(2,0), (2,2), (3,1)]
    ]


def test_compute(unsorted_point_set):
    result = siatec.compute(unsorted_point_set, min_pattern_length=2)
    assert result == [
        [[(1,1), (1,3), (2,2)], [(2,1), (2,3), (3,2)]],
        [[(2,1), (2,2)], [(2,2), (2,3)]],
        [[(1,1), (2,1)], [(1,3), (2,3)], [(2,2), (3,2)]],
        [[(1,1), (2,1)], [(1,3), (2,3)], [(2,2), (3,2)]],
        [[(1,1), (2,1)], [(1,3), (2,3)], [(2,2), (3,2)]]
    ]