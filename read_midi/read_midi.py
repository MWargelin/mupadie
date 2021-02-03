import mido


def to_point_set(path, chosen_tracks):
	point_set = list()
	mid = mido.MidiFile(path)

	mid.tracks = [track for i, track in enumerate(mid.tracks) if i in chosen_tracks]

	note_onset = 0

	for msg in mid:
		note_onset += msg.time
		if msg.type == 'note_on' and msg.velocity != 0:
			point_set.append((note_onset, msg.note))

	return point_set


def tracks_enumerate(path):
    mid = mido.MidiFile(path)
    return enumerate(mid.tracks)
