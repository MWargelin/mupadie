// point_set is passed in the analyse.html file
var data = point_set

// set the dimensions and margins of the graph
const last_onset = data[data.length - 1][0]
var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = last_onset * 100 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// append the svg object to the page
var svg = d3.select("#point_set_vis")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

// Add X axis
var x = d3.scaleLinear()
    .domain([0, last_onset])
    .range([ 0, width ]);
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

// Add Y axis
const max_midi_pitch = 127
var y = d3.scaleLinear()
    .domain([0, max_midi_pitch])
    .range([ height, 0]);
svg.append("g")
    .call(d3.axisLeft(y));

// Add dots
svg.append("g")
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
        .attr("cx", function (d) { return x(d[0]); })
        .attr("cy", function (d) { return y(d[1]); })
        .attr("r", 2.5)
        .style("fill", "#006666")
