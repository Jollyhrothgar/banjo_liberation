from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from bl.auth import login_required
from bl.db import get_db
import bl.banjo as banjo

bp = Blueprint("rolls", __name__)


# Example progression: alpha_major_g5 alpha_major_c6 alpha_major_d6 alpha_major_g5
# Example roll pattern: T4I3M2T3I2M1T4I3M2T3I2M1T512T3M1

@bp.route("/rolls", methods=("GET", "POST"))
def rolls():
  """Generate some rolls"""
  if request.method == "POST":
    progression = request.form['progression']
    roll_pattern = request.form['roll']
    error = None
    if error is not None:
      flash(error)
    else:
      progression = [token.strip() for token in progression.split()]
      roll_pattern = roll_pattern.strip()
      print(f"Progression {progression}\nRoll: {roll_pattern}")

      progression = [banjo.CHORDS[p] for p in progression] 
      measures = banjo.roll_on_progression(progression=progression, roll_pattern=roll_pattern)
      ascii_tab = banjo.render_ascii_measures(measures)

      return render_template("music/rolls.html", ascii_tab=ascii_tab)
  return render_template("music/rolls.html")
