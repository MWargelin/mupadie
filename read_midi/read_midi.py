import mido


def to_point_set(path, chosen_tracks):
	point_set = set()
	mid = mido.MidiFile(path)

	mid.tracks = [track for i, track in enumerate(mid.tracks) if i in chosen_tracks]
	mid = mido.merge_tracks(mid.tracks)

	note_onset = 0
	tempo = 0
	for msg in mid:
		if msg.type == 'set_tempo':
			tempo = msg.tempo
		note_onset += msg.time * tempo
		if msg.type == 'note_on' and msg.velocity != 0:
			point_set.add((note_onset, msg.note))

	return sorted(point_set)


def tracks_enumerate(path):
    mid = mido.MidiFile(path)
    return enumerate(mid.tracks)
