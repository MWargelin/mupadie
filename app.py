import os
import json

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from read_midi import read_midi
from algorithms import siatec, time_warp_invariant

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'midi_files'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024	# Allow max. 1MB files
app.config['ALLOWED_EXTENSIONS'] = {'.mid', '.midi', '.json'}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', default='dev')


@app.route('/')
def index():
	"""Route for home page of the application."""
	return render_template('index.html')


def is_allowed_file_type(filename):
	"""Function for testing whether file type of an uploaded file
	is in the list of allowed file types.

	Args:
		filename: Name of the file.

	Returns:
		True if file type is allowed, false if not.
	"""
	ext = os.path.splitext(filename)[1]
	return ext in app.config['ALLOWED_EXTENSIONS']


def file_validation(file):
	"""Function that determines whether the uploaded file is valid or not.

	Args:
		file: Uploaded file.

	Returns:
		True if file is valid, false if not.
	"""
	# A file is chosen
	if file.filename == '':
		flash('File not chosen', 'danger')
		return False
		

	# The file is of allowed file type
	if not is_allowed_file_type(file.filename):
		flash('File is not a MIDI or JSON file', 'danger')
		return False

	# TODO: Add content validation?

	return True


@app.route('/upload', methods=['POST'])
def upload_file():
	"""Route to upload files."""

	f = request.files['file']

	if not file_validation(f):
		return redirect(url_for('index'))

	# When validations are passed, save file
	filename = secure_filename(f.filename)
	os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
	filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	f.save(filepath)
	flash('File uploaded succesfully', 'success')

	return redirect(url_for('analyse_file', filename=filename))


def _point_set_from_form(form, midi_filepath):
	"""Handles the form in which the user determines which tracks
	of the file to include, creating a point set representation of it.

	Args:
		form: The form data.
		midi_filepath: Filepath to the MIDI file.

	Returns:
		Point set according to the form sent by the user.
	"""
	selected_tracks = []
	prefix = 'track-'
	for key in form.keys():
		if key.startswith(prefix):
			selected_tracks.append(int(key[len(prefix):]))

	point_set = read_midi.to_point_set(midi_filepath, selected_tracks)

	return point_set


def _pattern_data_from_form(form, point_set):
	"""Handles the form in which the user determines which algorithms
	to run with the uploaded file, and computes the algorithm results.

	Args:
		form: The form data
		point_set: Point set representation of the uploaded file.

	Returns:
		Musical pattern discovery results of the algorithms
		chosen by the user.
	"""
	pattern_data = []

	# SIATEC
	min_pattern_length = form.getlist('siatec-min-pattern-length')
	min_pattern_length = [int(x) for x in min_pattern_length]
	for i in range(len(min_pattern_length)):
		pattern_data.append(
			siatec.compute(
				point_set=point_set,
				min_pattern_length=min_pattern_length[i]
			)
		)

	# timewarp-invariant algorithm
	window = form.getlist('timewarp-window')
	window = [int(x) for x in window]
	for i in range(len(window)):
		pattern_data.append(
			time_warp_invariant.compute(
				point_set=point_set,
				window=window[i]
			)
		)

	return pattern_data


@app.route('/analyse/<path:filename>', methods=['GET', 'POST'])
def analyse_file(filename):
	"""Route to the parameter settings and visualisation page."""

	ext = os.path.splitext(filename)[1]

	filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

	if ext == '.json':
		# User uploaded results in json form

		with open(filepath, 'r') as json_file:
			data = json.loads(json_file.read())
		tracks = None

	else:
		# User uploaded a MIDI file

		tracks = read_midi.tracks_enumerate(filepath)

		if request.method == 'POST':
			point_set = _point_set_from_form(request.form, filepath)
			pattern_data = _pattern_data_from_form(request.form, point_set)
			data = {'point_set': point_set, 'pattern_data': pattern_data}
		else:
			data = None

	return render_template('analyse.html', 
						   filename=filename,
						   tracks=tracks,
						   data=data)


@app.route('/json_instructions')
def json_instructions():
	"""Route to the page that describes how to upload algorithm
	results as JSON files to the application.
	"""
	return render_template('json_instructions.html')


if __name__ == '__main__':
	environment = os.environ.get('ENVIRONMENT', default='development')

	if environment == 'production':
		debug = False
	else:
		debug = True

	app.run(debug=debug)
