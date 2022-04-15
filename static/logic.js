
    let arenaInfo =  {{ arenaInfo|safe }}; 
    let arenaMarker = [];

    let myMap = L.map("map", {
   center: [37.09, -95.71],
   zoom: 5
 });


for (var i=0; i < arenaInfo.length; i++) {
  console.log(arenaMarker)
  arenaMarker.push(
L.marker(arenaInfo[i].location).bindPopup("<h1>"+arenaInfo[i].arenaName+" - Home of the"+arenaInfo[i].teamName+"</h1>").addTo(myMap)
  );
};

// Create a map object.



 // Add a tile layer.
 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(myMap)