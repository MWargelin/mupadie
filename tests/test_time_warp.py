from algorithms import time_warp_invariant


def test_relabel_x():
	point_set = [(1,1), (13,2), (13,3), (89,4)]
	relabeled, mapping = time_warp_invariant._relabel_x(point_set)

	assert relabeled == [(1,1), (2,2), (2,3), (3,4)]
	assert mapping[(1,1)] == (1,1)
	assert mapping[(2,2)] == (13,2)
	assert mapping[(2,3)] == (13,3)
	assert mapping[(3,4)] == (89,4)


def test_note_pair_groups(sorted_point_set):
	result = time_warp_invariant._note_pair_groups(sorted_point_set)

	assert result == {
		0: [((1,1), (1,1)), ((1,1), (2,1)), ((1,3), (1,3)), ((1,3), (2,3)), ((2,1), (1,1)), ((2,1), (2,1)), ((2,2), (2,2)), ((2,2), (3,2)), ((2,3), (1,3)), ((2,3), (2,3)), ((3,2), (2,2)), ((3,2), (3,2))],
		-2: [((1,1), (1,3)), ((1,1), (2,3)), ((2,1), (1,3)), ((2,1), (2,3))],
		-1: [((1,1), (2,2)), ((1,1), (3,2)), ((2,1), (2,2)), ((2,1), (3,2)), ((2,2), (1,3)), ((2,2), (2,3)), ((3,2), (1,3)), ((3,2), (2,3))],
		2: [((1,3), (1,1)), ((1,3), (2,1)), ((2,3), (1,1)), ((2,3), (2,1))],
		1: [((1,3), (2,2)), ((1,3), (3,2)), ((2,2), (1,1)), ((2,2), (2,1)), ((2,3), (2,2)), ((2,3), (3,2)), ((3,2), (1,1)), ((3,2), (2,1))]
	}


def test_process_group():
	group = [
		((0,0), (1,2)),
		((2,1), (5,3)),
		((1,1), (4,3)),
		((1,1), (5,3)),
		((2,1), (4,3))
	]

	pattern1 = [(0,0), (1,1), (2,1)]
	pattern2 = [(1,2), (4,3), (5,3)]

	result = time_warp_invariant._process_group(group, window=999)
	assert [pattern1, pattern2] in result


def test_process_group_with_window():
	group = [
		((0,0), (1,2)),
		((2,1), (5,3)),
		((1,1), (4,3)),
		((1,1), (5,3)),
		((2,1), (4,3))
	]

	pattern1 = [(1,1), (2,1)]
	pattern2 = [(4,3), (5,3)]

	result = time_warp_invariant._process_group(group, window=1)
	assert [pattern1, pattern2] in result


def test_format_for_visualisation_meta_text():
	window = 0
	min_pattern_length = 1
	result = time_warp_invariant._format_for_visualisation([], window, min_pattern_length)
	assert result['meta'] == 'Transposition and time-warp invariant algorithm. Minimum pattern length: 1. Window: unrestricted'

	window = 1
	min_pattern_length = 1
	result = time_warp_invariant._format_for_visualisation([], window, min_pattern_length)
	assert result['meta'] == 'Transposition and time-warp invariant algorithm. Minimum pattern length: 1. Window: 1'

	window = 1
	min_pattern_length = 2
	result = time_warp_invariant._format_for_visualisation([], window, min_pattern_length)
	assert result['meta'] == 'Transposition and time-warp invariant algorithm. Minimum pattern length: 2. Window: 1'


def test_compute():
	point_set = [(0,0), (4,1), (2,1), (8,3), (2,2), (10,3)]
	results = time_warp_invariant.compute(point_set, window=0, min_pattern_length=1)
	pattern = [[(0,0), (2,1), (4,1)], [(2,2), (8,3), (10,3)]]
	assert pattern in results['patterns']
