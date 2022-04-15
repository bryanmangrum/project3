from re import A
from unittest import result
from flask import Flask, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import config

# Initial connection to database
engine = create_engine(f"postgresql://postgres:{config.pw}@localhost:5432/{config.db}")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reflect tables
Player_Salaries = Base.classes.player_2020_salaries
Win_Counts = Base.classes.win_counts
Team_Attributes = Base.classes.team_attributes
Draft = Base.classes.draft
Arenas = Base.classes.arenas

# Initialize app
app = Flask(__name__)


@app.route("/")
def index():
    session = Session(engine)
    #results = session.query(Team_Attributes.arena).all()
    arenaInfo = []
    result = session.query(Arenas.latitude, Arenas.longitude, Arenas.arena, Arenas.team, Arenas.arenaurl ,Arenas.sponsorurl)
    for row in result:
        latlon = []
        latlon.append(row[0])
        latlon.append(row[1])
        arena_dict = {
            "location": latlon,
            "arenaName": row[2],
            "teamName": row[3],
            "arenaURL": row[4],
            "sponsorURL": row[5]
        }
        arenaInfo.append(arena_dict)

    

    print(arenaInfo)
    


    session.close()

    return render_template("index.html", arenaInfo = arenaInfo)


@app.route("/salaries")
def salaries():
    # Initialize database session
    session = Session(engine)

    # Base labels and parents
    labels = ["League", "Western Conference", "Eastern Conference"]
    parents = ["", "League", "League"]

    # Query for distinct divisions and their parent conferences
    results = session.query(Win_Counts.division, Win_Counts.conference)\
        .distinct()

    for row in results:
        # append distinct divisions to labels
        labels.append(row[0])
        # append their parent conferences to parents
        parents.append(row[1])

    # Query distinct teams
    team_results = session.query(Win_Counts.team, Win_Counts.division)\
        .distinct()

    for row in team_results:
        # append distinct teams to labels
        labels.append(row[0])
        # append their parent divisions to parents
        parents.append(row[1])
        # new query using current row's team name
        player_results = session.query(
            Player_Salaries.player,
            Player_Salaries.team
        ).filter(Player_Salaries.team == row[0])
        for player in player_results:
            # append distinct players into labels
            labels.append(player[0])
            # append parent team into parents
            parents.append(player[1])

    # Close connection
    session.close()

    return render_template("salaries.html", labels=labels, parents=parents)


if __name__ == "__main__":
    app.run(debug=True)
