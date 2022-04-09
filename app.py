from flask import Flask, render_template

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column, Integer, String

# Initial connection to sqlite database
engine = create_engine("postgresql://postgres:password@localhost:5432/basketball")
Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Reflect tables
# Div_Conf = Base.classes.Div_Conf
# Player_Salaries = Base.classes.Player_2020_Salaries
# Win_Counts = Base.classes.Win_Counts
# Team_Attributes = Base.classes.Team_Attributes

# Initialize app
app = Flask(__name__)


@app.route("/")
def index():
    print("you're in home")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
