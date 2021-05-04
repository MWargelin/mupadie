import mido
from flask import flash


def to_point_set(path, chosen_tracks):
	"""Produce a point set representation of MIDI file in given path.

	Args:
		path: path to the MIDI file
		chosen_tracks: list of track numbers that the user wants to
		be included in the point set

	Returns:
		Point set representation of MIDI file in given path. The point
		set is a list of notes, and notes are tuples of note onset and
		MIDI pitch number
	"""
	point_set = set()
	mid = mido.MidiFile(path)
	mid = _filter_tracks(mid, chosen_tracks)
	mid = mido.merge_tracks(mid.tracks)

	note_onset = 0
	tempo = 1
	for msg in mid:
		if msg.type == 'set_tempo':
			tempo = msg.tempo
		note_onset += msg.time * tempo
		if msg.type == 'note_on' and msg.velocity != 0:
			point_set.add((note_onset, msg.note))

	point_set = sorted(point_set)
	point_set = _limit_point_set_length(point_set, 1000)

	return point_set


def _filter_tracks(mid, chosen_tracks):
	"""Turn the velocity of all notes in not chosen tracks to 0,
	so that the notes don't get picked up when reading the point set.
	This is done to avoid having to delete the tracks completely -
	deleting the tracks leads to a bug when removing the first track
	of a file.

	Args:
		mid: MIDI object
		chosen_tracks: the track numbers of the tracks that the user
		wants to be included in the point set in a list

	Returns:
		The given MIDI object, with the not chosen tracks filtered out
	"""
	for i, track in enumerate(mid.tracks):
		if i not in chosen_tracks:
			for msg in track:
				if msg.type == 'note_on':
					msg.velocity = 0
	return mid


def _limit_point_set_length(point_set, limit):
	"""Limit the length of point set by the given limit
	in order to not crash the program with too
	long inputs. If point set is to be limited, user is informed
	with a flash message.

	Args:
		point_set: The point_set to be limited
		limit: maximum number of notes in the limited point set

	Returns:
		The given point set limited to contain the number of notes
		specified in given limit. The notes in order from the beginning
		of the piece remain, while notes from the end are filtered out.
	"""
	if len(point_set) > limit:
		flash(f'Input was limited to {limit} notes to avoid crashing', 'warning')

	return point_set[:limit]


def tracks_enumerate(path):
	"""Get enumerated tracks of MIDI file in given path.

	Args:
		path: path to the MIDI file

	Returns:
		Enumerated tracks of the MIDI file
	"""
	mid = mido.MidiFile(path)
	return enumerate(mid.tracks)
