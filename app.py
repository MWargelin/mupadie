import os

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from read_midi import read_midi

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'midi_files'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024	# Allow max. 1MB files
app.config['ALLOWED_EXTENSIONS'] = {'.mid', '.midi'}
app.config['SECRET_KEY'] = 'computationalmusicology'


@app.route('/')
def index():
	return render_template('index.html')


def is_allowed_file_type(filename):
	"""Function for testing whether file type is in the list
	of allowed file types"""
	ext = os.path.splitext(filename)[1]
	return ext in app.config['ALLOWED_EXTENSIONS']


def file_validation(file):
	# A file is chosen
	if file.filename == '':
		flash('File not chosen', 'danger')
		return False
		

	# The file is midi file
	if not is_allowed_file_type(file.filename):
		flash('File is not a MIDI file', 'danger')
		return False

	# TODO: Add content validation?

	return True


@app.route('/upload', methods=['POST'])
def upload_file():
	"""Route to upload MIDI files to be analysed."""

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


@app.route('/analyse/<path:filename>')
def analyse_file(filename):
	midi_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	point_set = read_midi.to_point_set(midi_filepath)
	# plot_img_path = read_midi.create_plot(point_set)
	return render_template('analyse.html', 
						   filename=filename,
						   point_set=point_set,
						   # plot_img_path=plot_img_path
						  )


if __name__ == '__main__':
	app.run(debug=True)
