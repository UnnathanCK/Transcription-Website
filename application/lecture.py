from flask import (
    Blueprint, flash, jsonify, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from application import questions_db
from application.auth import login_required
from . import transcript
from . import questions_db as q_db

import threading

bp = Blueprint('lecture', __name__)

@bp.route('/')
def index():
    # q_db = questions_db.get_db()
    # # questions = q_db.execute(
    # #     'SELECT q.id, author_id, body, created, username'
    # #     ' FROM question q JOIN user u ON q.author_id = u.id'
    # #     ' ORDER BY created DESC'
    # # ).fetchall()
    return redirect(url_for('lecture.student'))

@bp.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        question_text = request.form['question-input']

        db = q_db.get_db()
        error = None

        if not question_text:
            error = 'Question text is required.'

        if error is None:
            db.execute(
                'INSERT INTO question (body) VALUES (?)',
                (question_text,)
            )
            db.commit()

    return render_template('lecture/student.html')


# Transcription Stuff
transcript_lines = []
transcript_lock = threading.Lock()

def save_transcription(text):
    #print("TRANSCRIPTION RECEIVED:", text)
    
    with transcript_lock:
        transcript_lines.append(text)

@bp.route("/start-captions", methods=["POST"])
def start_captions():
    try:
        with transcript_lock:
            transcript_lines.clear()

        transcript.start(on_transcription=save_transcription)

        return jsonify({"status": "started"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@bp.route("/stop-captions", methods=["POST"])
def stop_captions():
    try:
        transcript.stop()
        return jsonify({"status": "stopped"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@bp.route("/transcript", methods=["GET"])
def get_transcript():
    with transcript_lock:
        return jsonify({"lines": transcript_lines.copy()})


@bp.route('/questions', methods=['GET'])
def get_questions():
    db = q_db.get_db()

    questions = db.execute(
        'SELECT body FROM question ORDER BY rowid ASC'
    ).fetchall()

    return jsonify({
        'questions': [question['body'] for question in questions]
    })