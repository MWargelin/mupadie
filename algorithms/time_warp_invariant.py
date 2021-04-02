from collections import defaultdict


def compute(point_set):
	point_set.sort()
	relabeled_set, mapping = _relabel_x(point_set)
	note_pairs = _note_pair_groups(relabeled_set)
	patterns = []
	for group in note_pairs.values():
		patterns.append(_process_group(group))

	# Map notes back to the original notes
	for instances in patterns:
		for i in range(len(instances)):
			mapped = [mapping[note] for note in instances[i]]
			instances[i] = mapped

	return _format_for_visualisation(patterns)


def _relabel_x(point_set):
	"""Relabels note onsets of the given point set.

	The note onsets relabeled to be integers in between 1 and the length of
	the point set. Returns the relabeled set, and a mapping dictionary with
	relabeled notes as keys and original points as the values.

	Assumes that the given point set is sorted.
	"""
	relabeled_set = []
	mapping = {}
	relabel_onset = 1
	old_onset = point_set[0][0]

	for point in point_set:
		if point[0] != old_onset:
			relabel_onset += 1

		old_onset = point[0]
		relabeled_point = (relabel_onset, point[1])
		relabeled_set.append(relabeled_point)
		mapping[relabeled_point] = point

	return relabeled_set, mapping


def _note_pair_groups(point_set):
	note_pairs = defaultdict(list)

	for x in point_set:
		for y in point_set:
			# if x == y:
			# 	continue
			interval = x[1] - y[1]
			note_pairs[interval].append((x, y))

	return note_pairs


def _process_group(group):
	group.sort(key=lambda pair: (pair[0][0], pair[1][0]))

	arr = [(pair[0][0], pair[1][0]) for pair in group]

	n = len(arr)

	lis = [1] * n
	index = [None] * n

	for i in range(1, n):
		for j in range(0, i):
			if arr[i][0] > arr[j][0] and arr[i][1] > arr[j][1] and lis[i] < lis[j] + 1:
				lis[i] = lis[j] + 1
				index[i] = j

	pos = lis.index(max(lis))

	seq = []
	while (pos != None):
		seq.append(group[pos])
		pos = index[pos]
	seq.reverse()

	instance1 = [pair[0] for pair in seq]
	instance2 = [pair[1] for pair in seq]
	pattern = [instance1, instance2]
	return pattern


def _format_for_visualisation(patterns):
	return {
		'meta': 'Transposition and time-warp invariant algorithm',
		'patterns': patterns
	}
