from flask import Flask, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql.expression import cast
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Integer
import numpy as np

# Initial connection to database

engine = create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reflect tables
Player_Salaries = Base.classes.player_2020_salaries
Win_Counts = Base.classes.win_counts
Team_Attributes = Base.classes.team_attributes
Draft = Base.classes.draft
Arenas = Base.classes.arenas
Colors = Base.classes.colors

# Initialize app
app = Flask(__name__)


@app.route("/")
def index():
    session = Session(engine)
    arenaInfo = []
    result = session.query(Arenas.latitude, Arenas.longitude, Arenas.arena,
                           Arenas.team, Arenas.arenaurl, Arenas.sponsorurl)
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

    session.close()

    return render_template("index.html", arenaInfo=arenaInfo)

@app.route("/salaries")
def salaries():
    # Initialize database session
    session = Session(engine)

    # Base labels and parents
    labels = ["League", "Western Conference", "Eastern Conference"]
    parents = ["", "League", "League"]
    values = []

    # Query for league salary total (add up all players' salaries)
    results = session.query(func.sum(Player_Salaries.salary))
    values.append(results[0][0])

    # Query for conference salary total
    for conference in labels[1:]:
        conference_total = session.query(func.sum(Player_Salaries.salary))\
            .join(Win_Counts, Player_Salaries.team == Win_Counts.team)\
            .group_by(Win_Counts.conference)\
            .having(Win_Counts.conference == conference)
        for total in conference_total:
            values.append(total[0])

    # Query for distinct divisions and their parent conferences
    results = session.query(Win_Counts.division, Win_Counts.conference)\
        .distinct()

    for row in results:
        # append distinct divisions to labels
        labels.append(row[0])
        # append their parent conferences to parents
        parents.append(row[1])
        # find salary totals for division
        division_total = session.query(func.sum(Player_Salaries.salary))\
            .join(Win_Counts, Player_Salaries.team == Win_Counts.team)\
            .group_by(Win_Counts.division)\
            .having(Win_Counts.division == row[0])
        values.append(division_total[0][0])

    # Query distinct teams
    team_results = session.query(Win_Counts.team, Win_Counts.division)\
        .distinct()

    for row in team_results:
        # append distinct teams to labels
        labels.append(row[0])
        # append their parent divisions to parents
        parents.append(row[1])
        # find salary totals for team
        team_total = session.query(func.sum(Player_Salaries.salary))\
            .join(Win_Counts, Player_Salaries.team == Win_Counts.team)\
            .group_by(Win_Counts.team)\
            .having(Win_Counts.team == row[0])
        values.append(team_total[0][0])
        # new query using current row's team name
        player_results = session.query(
            Player_Salaries.player,
            Player_Salaries.team,
            Player_Salaries.salary
        ).filter(Player_Salaries.team == row[0])
        for player in player_results:
            # append distinct players into labels
            labels.append(player[0])
            # append parent team into parents
            parents.append(player[1])
            # append salary into values
            values.append(player[2])

    # Close connection
    session.close()

    return render_template(
        "salaries.html",
        labels=labels,
        parents=parents,
        values=values
    )


@app.route("/wins")
def wins():
    # Initialize database session
    session1 = Session(engine)

    # For Team Win_Counts
    # Base labels and parents
    label = ["League", "Eastern Conference", "Western Conference"]
    parent = ["", "League", "League"]
    value = []
    colors = ["#FFFFFF","#1E56A0", "#FF165D", "#9D0191", "#C70039", "#350B40", "#283C63", "#004445", "#126E82"]

    # Get league total wins
    results = session1.query(func.sum(Win_Counts.win_count))
    value.append(results[0][0])

    # Query for distinct divisions and their parent conferences
    results = session1.query(
        Win_Counts.division,
        Win_Counts.conference
    ).distinct().order_by(Win_Counts.division)

    for row in results:
        # append distinct divisions to labels
        label.append(row[0])
        # append their parent conferences to parents
        parent.append(row[1])

    # Query distinct teams
    team_results = session1.query(Win_Counts.team, Win_Counts.division)\
        .distinct().order_by(Win_Counts.team)

    for row in team_results:
        # append distinct teams to labels
        label.append(row[0])
        # append their parent divisions to parents
        parent.append(row[1])

    team_colors = session1.query(Colors.color1, Colors.team).distinct().order_by(Colors.team)
    for color in team_colors:
        colors.append(f"#{color[0]}")


    win_totals1 = session1.query(
        func.sum(Win_Counts.win_count),
        Win_Counts.conference
    ).group_by(Win_Counts.conference).order_by(Win_Counts.conference)
    
    for row in win_totals1:
        value.append(row[0])

    win_totals2 = session1.query(
        func.sum(Win_Counts.win_count),
        Win_Counts.division
    ).group_by(Win_Counts.division).order_by(Win_Counts.division)
    
    for row in win_totals2:
        value.append(row[0])

    win_totals3 = session1.query(
        func.sum(Win_Counts.win_count),
        Win_Counts.team
    ).group_by(Win_Counts.team).order_by(Win_Counts.team)
    
    for row in win_totals3:
        value.append(row[0])

    # Close connection
    session1.close()

    return render_template("wins.html", label=label, parent=parent, value=value, colors=colors)


@app.route("/ratio")
def ratio():
    # Initialize database session
    session2 = Session(engine)

    #For Team Win_Counts
    # Base labels and parents
    label1 = ["League", "Eastern Conference", "Western Conference"]
    parent1 = ["", "League", "League"]
    value1 = []
    value2 = [1089]
    colors = ["#FFFFFF","#1E56A0", "#FF165D", "#9D0191", "#C70039", "#350B40", "#283C63", "#004445", "#126E82"]

    # Query for league salary total (add up all players' salaries)
    results = session2.query(func.sum(Player_Salaries.salary))
    value1.append(results[0][0])

    # Query for conference salary total
    for conference in label1[1:]:
        conference_total = session2.query(func.sum(Player_Salaries.salary))\
            .join(Win_Counts, Player_Salaries.team == Win_Counts.team)\
            .group_by(Win_Counts.conference)\
            .having(Win_Counts.conference == conference)
        for total in conference_total:
            value1.append(total[0])

    # Query for distinct divisions and their parent conferences
    results = session2.query(Win_Counts.division, Win_Counts.conference)\
        .distinct().order_by(Win_Counts.division)

    for row in results:
        # append distinct divisions to labels
        label1.append(row[0])
        # append their parent conferences to parents
        parent1.append(row[1])
        # find salary totals for division
        division_total = session2.query(func.sum(Player_Salaries.salary))\
            .join(Win_Counts, Player_Salaries.team == Win_Counts.team)\
            .group_by(Win_Counts.division)\
            .having(Win_Counts.division == row[0])
        value1.append(division_total[0][0])

    # Query distinct teams
    team_results = session2.query(Win_Counts.team, Win_Counts.division)\
        .distinct().order_by(Win_Counts.team)

    for row in team_results:
        # append distinct teams to labels
        label1.append(row[0])
        # append their parent divisions to parents
        parent1.append(row[1])
        # find salary totals for team
        team_total = session2.query(func.sum(Player_Salaries.salary))\
            .join(Win_Counts, Player_Salaries.team == Win_Counts.team)\
            .group_by(Win_Counts.team)\
            .having(Win_Counts.team == row[0])
        value1.append(team_total[0][0])

    team_colors = session2.query(Colors.color1, Colors.team).distinct().order_by(Colors.team)
    for color in team_colors:
        colors.append(f"#{color[0]}")

    win_totals1 = session2.query(func.sum(Win_Counts.win_count), Win_Counts.conference).group_by(Win_Counts.conference).order_by(Win_Counts.conference)
    
    for row in win_totals1:
        value2.append(row[0])

    win_totals2 = session2.query(func.sum(Win_Counts.win_count), Win_Counts.division).group_by(Win_Counts.division).order_by(Win_Counts.division)
    
    for row in win_totals2:
        value2.append(row[0])

    win_totals3 = session2.query(func.sum(Win_Counts.win_count), Win_Counts.team).group_by(Win_Counts.team).order_by(Win_Counts.team)
    
    for row in win_totals3:
        value2.append(row[0])

    value3 = list(np.around(np.true_divide(value1, value2), decimals=0))
    print(value3)


    # Close connection
    session2.close()

    return render_template("ratio.html", labels=label1, parents=parent1, values=value3, colors=colors)


if __name__ == "__main__":
    app.run(debug=True)
