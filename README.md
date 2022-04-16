# The Relationship Between Player Salaries and Team Wins for the 2020-2021 NBA Season

This project started with the idea that we wanted to see if team investments into their rosters translated to wins on the court. This is with the understanding that money spent is not the only factor that goes into a team's success or failure. We looked at NBA teams for the 2020-2021 season and analyzed their wins, the money spent on player salaries, and [the relationship between those two](https://money-in-the-nba.herokuapp.com).

We first wanted to incorporate Leaflet and a map into our product, so we thought to include the [location of each team's home arena](https://docs.google.com/presentation/d/1mqYkSCEXJvSyd6BqcCEc-TgwN9aE_Kg7fApw-117O7s/edit#slide=id.g1248e664244_1_21). We leveraged GoogleMaps for the location data of each arena, and then linked the markers to a .png with each team's logo to replace the standard marker.

![Map of Arenas](/readme_images/arena_map.png)

We also added a popup upon clicking each marker that displayed the arena's name which was embedded with a link to the arena, a link to the sponsor of the arena, and which business sector the sponsor was a part of.

![Map with Marker Selected](/readme_images/arena_map_link.png)

We also included a [breakdown of sponsors by business sector](https://docs.google.com/presentation/d/1mqYkSCEXJvSyd6BqcCEc-TgwN9aE_Kg7fApw-117O7s/edit#slide=id.g1248e664244_1_50) and our findings reflected the current business environment, dominated by financial and technology based institutions.

![Sponsors by Business Sector](/readme_images/sponsor_sector.png)

Salaries were the next aspect that we wanted to focus on. We were able to find a SQLite file that contained a wealth of NBA data, including player salaries for the 2020-21 season. In Flask using SQLAlchemy, we queried the data ([after extensive cleaning and a migration to a PostgreSQL server](/readme_images/code_snippet.png)) to find [the amount spent by teams](https://docs.google.com/presentation/d/1mqYkSCEXJvSyd6BqcCEc-TgwN9aE_Kg7fApw-117O7s/edit#slide=id.g1248e664244_1_11) with breakdowns from the Conference level all the way down to the player level.

![Salary Sunburst Visualization](/readme_images/salaries_sunburst_base.png)

![Salary Sunburst Visualization Granularity](/readme_images/salaries_sunburst_granular.png)

Next we looked at wins in a similar breakdown to salaries. We did not go as granular as wins as a player stat didn't really make sense. Using a similar method [we grouped wins by Conference, then Division, then ultimately team](https://docs.google.com/presentation/d/1mqYkSCEXJvSyd6BqcCEc-TgwN9aE_Kg7fApw-117O7s/edit#slide=id.g1248e664244_1_16). 

![Wins by Conference](/readme_images/wins_treemap.png)

![Wins by Team](/readme_images/wins_treemap_granular.png)

Finally, we looked at the ratio of dollars spent on salary to team wins. Using Numpy we were able to divide the salaries by the wins and after some trial and error get them to correlate correctly to their teams. We were originally going to display them as another treemap, but we decided that a [barchart simply broken out by team](https://docs.google.com/presentation/d/1mqYkSCEXJvSyd6BqcCEc-TgwN9aE_Kg7fApw-117O7s/edit#slide=id.g1248e664244_1_36) was the best way to represent this data. 

![Dollars Spent to Wins Bar Chart](/readme_images/ratio_bar_graph.png)

This project was challenging, interesting, trying, insightful, and a lot of fun to work on. Below are links to our full presentation, as well as our datasources and the different libraries we used to make this product possible. Thank you for checking out our app.

[Presentation](https://docs.google.com/presentation/d/1mqYkSCEXJvSyd6BqcCEc-TgwN9aE_Kg7fApw-117O7s/edit?usp=sharing)

[Plotly](https://plotly.com/javascript/)

[Chart.js](https://www.chartjs.org/)

[Leaflet](https://leafletjs.com/)

[Flask](https://flask.palletsprojects.com/en/2.1.x/)

[SQLAlchemy](https://www.sqlalchemy.org/)

[Numpy](https://numpy.org/)

[Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/)

[NBA Player Salaries Data](http://www.espn.com/nba/salaries/_/year/2021/)

[NBA Team Colors](https://teamcolorcodes.com/nba-team-color-codes/#What_Are_the_HEX_Color_Codes_Used_by_NBA_Teams)

[Team Logos](https://www.stickpng.com/cat/sports/basketball/nba-teams)

[NBA Team Wins Dataset](https://www.kaggle.com/datasets/wyattowalsh/basketball)

Created by: Charles Phil, Coye Roseberry, Shawn Varghese, Bryan Mangrum


