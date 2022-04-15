from flask import Flask, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Initial connection to database
engine = create_engine("postgresql://postgres:postgres@localhost:5432"
                       "/postgres")
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
    results = session.query(Team_Attributes.arena).all()
    session.close()

    return render_template("index.html")


@app.route("/salaries")
def salaries():
    # Initialize database session
    session = Session(engine)

    # Base labels and parents
    labels = ["League", "Western Conference", "Eastern Conference"]
    parents = ["", "League", "League"]
    #values = []

    # Query for distinct divisions and their parent conferences
    results = session.query(Win_Counts.division, Win_Counts.conference)\
        .distinct().order_by(Win_Counts.division.desc())

    for row in results:
        # append distinct divisions to labels
        labels.append(row[0])
        # append their parent conferences to parents
        parents.append(row[1])

    # Query distinct teams
    team_results = session.query(Win_Counts.team, Win_Counts.division)\
        .distinct().order_by(Win_Counts.team.desc())

    for row in team_results:
        # append distinct teams to labels
        labels.append(row[0])
        # append their parent divisions to parents
        parents.append(row[1])
        # new query using current row's team name
        player_results = session.query(
            Player_Salaries.player,
            Player_Salaries.team
        ).filter(Player_Salaries.team == row[0]).order_by(Player_Salaries.team.desc())
        for player in player_results:
            # append distinct players into labels
            labels.append(player[0])
            # append parent team into parents
            parents.append(player[1])

        # Close connection
    session.close()

    return render_template("salaries.html", labels=labels, parents=parents)

@app.route("/wins")
def wins():
    # Initialize database session
    session1 = Session(engine)

    #For Team Win_Counts
    # Base labels and parents
    label = ["League", "Western Conference", "Eastern Conference"]
    parent = ["", "League", "League"]
    value = [""]

    # Query for distinct divisions and their parent conferences
    results = session1.query(Win_Counts.division, Win_Counts.conference).distinct().order_by(Win_Counts.division.desc())

    for row in results:
        # append distinct divisions to labels
        label.append(row[0])
        # append their parent conferences to parents
        parent.append(row[1])

    # Query distinct teams
    team_results = session1.query(Win_Counts.team, Win_Counts.division)\
        .distinct().order_by(Win_Counts.team.desc())

    for row in team_results:
        # append distinct teams to labels
        label.append(row[0])
        # append their parent divisions to parents
        parent.append(row[1])

    win_totals1 = session1.query(func.sum(Win_Counts.win_count), Win_Counts.conference).group_by(Win_Counts.conference).order_by(Win_Counts.conference.desc())
    
    for row in win_totals1:
        value.append(row[0])

    win_totals2 = session1.query(func.sum(Win_Counts.win_count), Win_Counts.division).group_by(Win_Counts.division).order_by(Win_Counts.division.desc())
    
    for row in win_totals2:
        value.append(row[0])

    win_totals3 = session1.query(func.sum(Win_Counts.win_count), Win_Counts.team).group_by(Win_Counts.team).order_by(Win_Counts.team.desc())
    
    for row in win_totals3:
        value.append(row[0])

    #print(value)


    # Close connection
    session1.close()

    return render_template("wins.html", label=label, parent=parent, value=value)


if __name__ == "__main__":
    app.run(debug=True)
