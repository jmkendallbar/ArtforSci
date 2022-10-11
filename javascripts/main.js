console.log("Hello from Javascript")
// alert("Welcome to Art for Science Communication!")

let portfolio = [
    {artist_src: "https://avatars0.githubusercontent.com/u/57967704?v=4&s=128", artist: "Jessica Kendall-Bar", project: "Elephant Seal Animation"},
    {artist_src: "https://avatars0.githubusercontent.com/u/57967704?v=4&s=128", artist: "Jessica Kendall-Bar", project: "Elephant Seal Animation"},
    {artist_src: "https://avatars0.githubusercontent.com/u/57967704?v=4&s=128", artist: "Jessica Kendall-Bar", project: "Elephant Seal Animation"},
    {artist_src: "https://avatars0.githubusercontent.com/u/57967704?v=4&s=128", artist: "Jessica Kendall-Bar", project: "Elephant Seal Animation"},
  ]
console.log(portfolio)

let sel = d3.select("#gallery")
.selectAll("div")
.data(portfolio)
.join("div")

sel.append("p").text((d) => d.artist)  /* d.species ? d.species : "don't know" */
sel.append("img").attr("src", d => d.artist_src).attr("title", d => d.artist)
.style("max-width", "400px")

// Now let's try with a csv

let csv_data = d3.csv("/data/artists_data.csv", function(data) {
    for (var i = 0; i < data.length; i++) {
        console.log(data[i].artist_src);
        console.log(data[i].project);
    }
});

csv_data.then(function(result){
    console.log(result)
});

console.log(csv_data)

// Fetch example with local file using .then method
// console.log("about to fetch kelp picture saved as algae.jpg in data folder")
// fetch("/data/algae.jpg").then(response => { // Call fetch function with a local path to image 
//     console.log(response);
//     return response.blob(); // then we get a response
// }).then(kelp_blob => {
//     console.log(kelp_blob); // grab the data in the response
//     document.getElementById('kelp').src = URL.createObjectURL(kelp_blob); // update img element with your data
// }).catch(error => { //Logging errors
//     console.log("Error! See below.") //Printing text to show error
//     console.error(error); //Showing error message
// });

// Fetch example with local file using async and await instead of code above
async function catchKelp() {
    const response = await fetch("/data/algae.jpg");
    const kelp_blob = await response.blob();
    document.getElementById('kelp').src = URL.createObjectURL(kelp_blob); // update img element with your data
}

// Calling the asynchronous function to display the fetched picture
catchKelp()
    .then(response => {
        console.log('yay kelp')
    })
    .catch(error => { //Logging errors
    console.log("Error with kelp image! See below.") //Printing text to show error
    console.error(error); //Showing error message
});

// Now fetching Elephant Seal Census data from a CSV
// Data cleaned from https://datadryad.org/stash/dataset/doi:10.7291/D1PP47

async function getData() {
    const response = await fetch("/data/Elephant Seal Census Data_small.csv");
    const census_data = await response.text();
    // console.log(census_data); // Preview data
    // Now parsing the data with separators
    const table = census_data.split('\n').slice(1); 
    // Using \n to show us where each new line is and taking out first row
    // then write .forEach loop
    table.forEach(row => {
        const columns = row.split(',');
        const Census_ID = columns[0]; // Naming columns
        const Observer = columns[1]; 
        const agesexclass = columns[9];
        const population = columns[11];
        xlabels.push(Census_ID);
        pop_estimate.push(population);
        // console.log(Census_ID,Observer);
    });
};

getData()
    .then(response => {
    console.log('yay data') // Celebrating successful data input
}).catch(error => { // Catching errors
    console.log("Error with data input! See below.") // Printing message to show error
    console.error(error); // Showing error message
});

const xlabels = [];
const pop_estimate = [];

// MakeChart();

// // Charting example with Chart.js
// async function MakeChart() {
//     await getData()
//     const ctx = document.getElementById('chart').getContext('2d');
//     const myChart = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: xlabels,
//             datasets: [{
//                 label: 'Population Estimate',
//                 data: pop_estimate,
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.2)',
//                     'rgba(54, 162, 235, 0.2)',
//                     'rgba(255, 206, 86, 0.2)',
//                     'rgba(75, 192, 192, 0.2)',
//                     'rgba(153, 102, 255, 0.2)',
//                     'rgba(255, 159, 64, 0.2)'
//                 ],
//                 borderColor: [
//                     'rgba(255, 99, 132, 1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(255, 206, 86, 1)',
//                     'rgba(75, 192, 192, 1)',
//                     'rgba(153, 102, 255, 1)',
//                     'rgba(255, 159, 64, 1)'
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 yAxes: [{
//                     ticks: {
//                         beginAtZero: true
//                     }
//                 }]
//             }
//         }
//     });
// }

const api_url = 'https://api.wheretheiss.at/v1/satellites/25544'
async function getISS() {
    const response = await fetch(api_url); //fetching API and storing in "response"
    const ISS_data = await response.json(); //putting response into ISS_data
    const {latitude, longitude} = ISS_data; //destructures JSON to put each into own variable
    console.log(ISS_data);
    document.getElementById('lat').textContent = latitude;
    document.getElementById('lon').textContent = longitude;
}

getISS();