import flask
from flask import request, jsonify

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=["POST"])
def add_jobs():
    js = request.json
    if not js:
        return {
            "Message": "У вас в json пусто"
        }
    else:
        sess = db_session.create_session()
        job = Jobs()
        # {"id": i.id,
        #                'team_leader': i.team_leader,
        #                'job': i.job,
        #                'work_size': i.work_size,
        #                'collaborators': i.collaborators,
        #                'start_date': i.start_date,
        #                'end_date': i.end_date,
        #                'is_finished': i.is_finished,
        #                }
        jobs = sess.query(Jobs).all()
        for i in jobs:
            if js["id"] == i.id:
                return {
                    "Error": " Id already exists."
                }
        job.id = js["id"]
        job.team_leader = js["team_leader"]
        job.job = js["job"]
        job.work_size = js["work_size"]
        job.collaborators = js["collaborators"]
        job.start_date = js["start_date"]
        job.end_date = js["end_date"]
        job.is_finished = js["is_finished"]
        sess.add(job)
        sess.commit()
        return {
            "Message": "OK"
        }


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    js = jsonify(
        {
            'users':
                [item.to_dict(only=(
                    "id",
                    'team_leader',
                    'job',
                    'work_size',
                    "collaborators",
                    "start_date",
                    "end_date",
                    "hashed_password",
                    "is_finished"))
                    for item in jobs]
        }
    )
    # js = {
    #     "jobs": []
    # }
    # for i in jobs:
    #     dic = {"id": i.id,
    #            'team_leader': i.team_leader,
    #            'job': i.job,
    #            'work_size': i.work_size,
    #            'collaborators': i.collaborators,
    #            'start_date': i.start_date,
    #            'end_date': i.end_date,
    #            'is_finished': i.is_finished,
    #            }
    #     js["jobs"].append(dic)
    return js


@blueprint.route('/api/jobs/<int:job_id>', methods=["PUT"])
def redact_one_job_id(job_id):
    try:
        js = request.json
        sess = db_session.create_session()
        job = sess.query(Jobs).filter().first()
        if not job:
            return {
                "Message": "Not found job"
            }
        job.id = js["id"]
        job.team_leader = js["team_leader"]
        # job.job = 1[""]
        job.work_size = js["work_size"]
        job.collaborators = js["collaborators"]
        job.start_date = js["start_date"]
        job.end_date = js["end_date"]
        job.is_finished = js["is_finished"]
        sess.commit()
        return {
            "Message": "OK"
        }
    except Exception:
        return "Ой здесь вылезла ошибочка"
# /api/jobs/<int:job_id>
@blueprint.route('/api/jobs/<int:job_id>', methods=["DELETE"])
def delete_one_job_id(job_id):
    try:
        sess = db_session.create_session()
        sess.query(Jobs).filter(Jobs.id == job_id).first().delete()
        sess.commit()
    except Exception:
        return "Ой здесь вылезла ошибочка"


@blueprint.route('/api/jobs/<int:job_id>')
def get_one_job_id(job_id):
    try:
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        # dic = {"id": jobs.id,
        #        'team_leader': jobs.team_leader,
        #        'job': jobs.job,
        #        'work_size': jobs.work_size,
        #        'collaborators': jobs.collaborators,
        #        'start_date': jobs.start_date,
        #        'end_date': jobs.end_date,
        #        'is_finished': jobs.is_finished,
        #        }
        js = jsonify(
            {
                'user':
                    jobs.to_dict(only=(
                    "id",
                    'team_leader',
                    'job',
                    'work_size',
                    "collaborators",
                    "start_date",
                    "end_date",
                    "hashed_password",
                    "is_finished"))
            }
        )
        return js
    except Exception:
        return "Неверный параметр или это моя ошибка"
