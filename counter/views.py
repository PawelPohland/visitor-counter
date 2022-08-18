from flask import Blueprint
from counter.models import Counter
from application import db

counter_app = Blueprint(name="counter_app", import_name=__name__)


@counter_app.route("/")
def init():
    counter = Counter.query.first()

    if not counter:
        counter = Counter(1)
        db.session.add(counter)
        db.session.commit()
    else:
        counter.count += 1
        db.session.commit()

    return f"<h1>Current counter value: {str(counter.count)}</h1>"
