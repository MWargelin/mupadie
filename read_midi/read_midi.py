import mido


def to_point_set(path):
	point_set = list()
	mid = mido.MidiFile(path)
	note_onset = 0

	for msg in mid:
		note_onset += msg.time
		if msg.type == 'note_on':
			if msg.velocity != 0:
				point_set.append((note_onset, msg.note))

    # TODO: Is the point set sorted?
	
	return point_set