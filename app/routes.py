from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from app.parser import extract_text_from_pdf
from app.scorer import score_cv

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/analyze', methods=['POST'])
def analyze():
    if 'cv_file' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('main.index'))

    file = request.files['cv_file']
    job_description = request.form.get('job_description', '').strip()

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('main.index'))

    if not job_description:
        flash('Please paste a job description')
        return redirect(url_for('main.index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        from flask import current_app
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            cv_text = extract_text_from_pdf(filepath)
            result = score_cv(cv_text, job_description)
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('main.index'))
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        return render_template('results.html', result=result)

    flash('Only PDF files are allowed')
    return redirect(url_for('main.index'))