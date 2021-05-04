from collections import defaultdict

def compute(point_set, min_pattern_length=2):
	"""Discover patterns from music using the SIATEC algorithm.

	Args:
		min_pattern_length: the minimum number of notes a pattern
			must have.

	Returns:
		Patterns discovered from the given point set using the
		SIATEC algorithm.
	"""
	point_set = sorted(point_set)
	mtps = _maximal_translatable_patterns(point_set, min_length=min_pattern_length)
	vector_table = _vector_table(point_set)
	translation_vectors = _translation_vectors(mtps, vector_table)
	result = _format_for_visualisation(translation_vectors, min_pattern_length)
	return result


def _vector_table(point_set):
	"""Computes a vector table for given point set.

	Vector table tells the distance of each point in the point set to
	all other points in the point set.

	Args:
		point_set: The point set to compute the vector table from

	Returns:
		A dictionary with origin point as key, and the list of translation vectors
		to all points in the point set as value.

	"""
	return {a:[ (b[0]-a[0], b[1]-a[1]) for b in point_set ] for a in point_set}


def _maximal_translatable_patterns(point_set, min_length=0):
	"""Returns maximal translatable patterns of the given point set.

	This is essentially the algorithm SIA: For each possible translation vector,
	return the largest set of points that can be translated by that vector to
	give another point in the point set.

	Args:
		point_set: The point set to use as input.
		min_length: The minimum number of notes in a pattern: if the maximal
			translatable pattern of a translation vector is smaller than this
			number, the pattern is discarded.

	Returns:
		A dictionary with translation vectors as keys and maximally translatable
		patterns as values.
	"""
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
	"""For a set of maximally translatable patterns, returns the set of
	translation vectors for the MTPs.

	Finds the common translation vectors for each note of a MTP, enabling
	finding all occurrences of the MTP.

	Args:
		mtps: All MTPs of a point set
		vector_table: vector table computed for the same point set that
			the MTPs are extracted from.

	Returns:
		All translation vectors for all MTPs of a point_set as a dictionary,
		where the original MTP is under the key 'pattern' and the translation
		vectors under the key 'translation_vectors'.
	"""
	translation_vectors = []
	for mtp in mtps.values():
		intersection = set(vector_table[mtp[0]])
		for point in mtp:
			intersection.intersection_update(set(vector_table[point]))
		translation_vectors.append({'pattern': mtp, 'translation_vectors': sorted(intersection)})
	return translation_vectors


def _get_instances(pattern, translation_vectors):
	"""Given a pattern and its translation vectors, translates the pattern by
	all those translation vectors.

	Args:
		pattern: the pattern to be translated
		translation_vectors: translation vectors for the pattern.

	Returns:
		A list of pattern instances, containing the original pattern translated
		by each of its translation vectors.
	"""
	instances = []
	for vector in translation_vectors:
		instances.append([(point[0] + vector[0], point[1] + vector[1]) for point in pattern])
	return instances


def _format_for_visualisation(translation_vectors, min_pattern_length):
	"""Transform the pattern discovery results into the specified data
	structure used in the Mupadie visualisation.

	Args:
		translation_vectors: All patterns and their translation vectors
			of a musical piece.
		min_pattern_length: the minimum pattern length parameter as set
			by the user of the application.

	Returns:
		A dictionary documenting the pattern discovery results.
	"""
	translation_vectors = sorted(translation_vectors,
								 key=lambda pattern: len(pattern['pattern']),
								 reverse=True)
	result = {'meta': f'SIATEC. Minimum pattern length: {min_pattern_length}'}
	result['patterns'] = [_get_instances(pattern['pattern'], pattern['translation_vectors'])
						  for pattern
						  in translation_vectors]
	return result
