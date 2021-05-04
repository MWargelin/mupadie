from collections import defaultdict


def compute(point_set, window=0):
	"""Discover patterns from music using a transposition and time-warp
	invariant algorithm.

	Args:
		window: The maximum number of notes there can be in between
		consecutive notes in a pattern. If window is set to 0, window
		is set to unrestricted mode, where there can be arbitrarily many
		notes between consecutive notes.

	Returns:
		Patterns discovered from the given point set using a time-warp
		and transposition invariant algorithm
	"""
	point_set.sort()
	relabeled_set, mapping = _relabel_x(point_set)
	note_pairs = _note_pair_groups(relabeled_set)
	patterns = []

	# window = 0 means unrestricted mode. Use length of the point set
	# as the window if this is the case, as that is enough for the window
	# to be unrestricted in practise.
	if window == 0:
		_window = len(point_set)
	else:
		_window = window

	# Find patterns
	for group in note_pairs.values():
		patterns.append(_process_group(group, _window))

	# Map notes in patterns back to the original notes
	for instances in patterns:
		for i in range(len(instances)):
			mapped = [mapping[note] for note in instances[i]]
			instances[i] = mapped

	return _format_for_visualisation(patterns, window)


def _relabel_x(point_set):
	"""Relabels note onsets of the given point set.

	The note onsets relabeled to be integers in between 1 and the length of
	the point set. Returns the relabeled set, and a mapping dictionary with
	relabeled notes as keys and original points as the values. Notes played
	originally at the same time get the same note onset value.

	Assumes that the given point set is sorted.

	Args:
		point_set: the point set to relabel

	Returns:
		a tuple: the point set relabeled, and a mapping dictionary with the
		relabeled points as keys and the original points as values
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
	"""Create all combinations of two notes in the point set and
	group them according to the interval between the note pair.

	Args:
		point_set: point set to use

	Returns:
		A dictionary with intervals as keys, with list of all note pairs in
		the given point set where the interval between the pair is the interval
		in the key as value
	"""
	note_pairs = defaultdict(list)

	for x in point_set:
		for y in point_set:
			# if x == y:
			# 	continue
			interval = x[1] - y[1]
			note_pairs[interval].append((x, y))

	return note_pairs


def _process_group(group, window):
	"""Find the longest pattern from given group

	Args:
		group: group of note pairs to find the longest pattern
		from
		window: the number of notes there can be in between
		consecutive notes of a pattern. Notes played at the
		same time are counted as "one note".

	Returns:
		The longest pattern in the group as a list of two
		items (first and second instance of the pattern)
	"""
	group.sort(key=lambda pair: (pair[0][0], pair[1][0]))

	arr = [(pair[0][0], pair[1][0]) for pair in group]

	n = len(arr)

	lis = [1] * n
	index = [None] * n

	for i in range(1, n):
		for j in range(0, i):
			if arr[i][0] > arr[j][0] and \
					arr[i][1] > arr[j][1] and \
					arr[i][0] - arr[j][0] <= window and \
					arr[i][1] - arr[j][1] <= window and \
					lis[i] < lis[j] + 1:
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


def _format_for_visualisation(patterns, window):
	"""Transform the pattern discovery results into the specified data
	structure used in the Mupadie visualisation.

	Args:
		patterns: the discovered patterns
		window: the window parameter as set by the user of the application

	Returns:
		A dictionary documenting the pattern discovery results
	"""
	if window == 0:
		window_string = 'unrestricted'
	else:
		window_string = window

	return {
		'meta': f'Transposition and time-warp invariant algorithm. Window: {window_string}',
		'patterns': patterns
	}
