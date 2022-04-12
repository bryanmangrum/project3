from flask import Flask, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Initial connection to sqlite database
engine = create_engine("postgresql://postgres:password@localhost:5432"
                       "/basketball")
Base = automap_base()
Base.prepare(engine, reflect=True)

# For debugging to see if our tables are in our Base
# print(Base.classes.keys())

# Reflect tables
Player_Salaries = Base.classes.player_2020_salaries
Win_Counts = Base.classes.win_counts
Team_Attributes = Base.classes.team_attributes
Draft = Base.classes.draft

# Initialize app
app = Flask(__name__)


@app.route("/")
def index():
    session = Session(engine)
    results = session.query(Team_Attributes.arena).all()
    session.close()

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
