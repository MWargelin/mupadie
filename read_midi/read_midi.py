import mido
from flask import flash


def to_point_set(path, chosen_tracks):
	point_set = set()
	mid = mido.MidiFile(path)
	mid = _filter_tracks(mid, chosen_tracks)

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
	"""
	for i, track in enumerate(mid.tracks):
		if i not in chosen_tracks:
			for msg in track:
				if msg.type == 'note_on':
					msg.velocity = 0
	return mid


def _limit_point_set_length(point_set, limit):
	"""Limit the length of point set by the number set in
	'limit' in order to not crash the program with too
	long inputs. If point set has to be limited, user is informed
	with a flash message.
	"""
	if len(point_set) > limit:
		flash('Input was limited to 1000 notes to avoid crashing', 'warning')

	return point_set[:limit]


def tracks_enumerate(path):
    mid = mido.MidiFile(path)
    return enumerate(mid.tracks)
