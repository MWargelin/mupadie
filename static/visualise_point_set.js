//// Data transformation, utility functions and constants
var data = point_set

const CIRCLE_RADIUS = 3
const PATTERN_CIRCLE_RADIUS = 5
const PATH_WIDTH = 4

function random_color() {
    color1 = Math.floor(Math.random() * 210)
    color2 = Math.floor(Math.random() * 210)
    color3 = Math.floor(Math.random() * 210)
    return "rgb("+color1+", "+color2+", "+color3+")"
}

pattern_xs = []
pattern_ys = []
data.patterns.forEach(pattern => {
    normalised = JSON.parse(JSON.stringify(pattern.instances[0]))
    const first_x = normalised[0][0];
    const first_y = normalised[0][1];
    normalised.forEach(point => {
        point[0] -= first_x
        point[1] -= first_y
        pattern_xs.push(point[0])
        pattern_ys.push(point[1])
    })
    pattern.normalised = normalised
})



//// Pattern selector
// Set the dimensions and margins of the graph
var pattern_width = 155
var pattern_height = 100
var pattern_margin = {top: 10, right: 10, bottom: 25, left: 10}

// If no patterns found, show message
if (data.patterns.length == 0) {
    d3.select("#patterns_div")
        .append("p")
            .text("No patterns found!")
            .style("width",  (pattern_width + pattern_margin.left + pattern_margin.right) + "px")
}

// Create small svg tags for patterns
pattern_divs = d3.select("#patterns_div")
    .selectAll("svg")
        .data(data.patterns)
        .enter()
        .append("div")

pattern_groups = pattern_divs
    .append("button")
        .attr("type", "button")
        .style("border-radius", "10px")
        .append("svg")
            .attr("width", pattern_width + pattern_margin.left + pattern_margin.right)
            .attr("height", pattern_height + pattern_margin.top + pattern_margin.bottom)
            .append("g")
                .attr("transform", "translate(" + pattern_margin.left + "," + pattern_margin.top + ")")

// Add pattern names
pattern_groups
    .append("text")
        .attr("text-anchor", "start")
        .attr("x", 0)
        .attr("y", pattern_height + 20)
        .text(function (d) { return d.name })

// Checkboxes to include patterns to visualisation
pattern_divs
    .append("input")
        .attr("type", "checkbox")
        .attr("class", "pattern-checkbox")
        .attr("id", function (d) { return "cb-" + d.name})

pattern_divs
    .append("label")
        .attr("for", function (d) { return "cb-" + d.name})
        .text(function (d) { return "Visualise " + d.name})

// Map extents of patterns for scaling patterns individually
xs_extent = d3.extent(pattern_xs)
ys_extent = d3.extent(pattern_ys)

var patterns_x_scale = d3.scaleLinear()
    .domain(xs_extent)
    .range([0, pattern_width])
var patterns_y_scale = d3.scaleLinear()
    .domain(ys_extent)
    .range([pattern_height, 0])

// Draw points for patterns
pattern_groups
    .selectAll("circle")
        .data(function(d) { return d.normalised })
        .enter()
        .append("circle")
            .attr("cx", function(d) { return patterns_x_scale(d[0]) })
            .attr("cy", function(d) { return patterns_y_scale(d[1]) })
            .style("fill", "#006666")
            .transition()
            .duration(1000)
            .attr("r", CIRCLE_RADIUS)

// Functionality to toggle showing patterns in main visualisation
function update_pattern_vis () {
    cb = d3.select(this)
    pattern_data = cb.datum()

    if (cb.property("checked")) {
        color = random_color()

        pattern_group = svg
            .append("g")
                .attr("class", function(d) { return pattern_data.name })
                .style("fill", function(d) { return color })
                .style("stroke", function(d) { return color })

        pattern_instances = pattern_group
            .selectAll(".pattern-instance")
                .data(function(d) { return pattern_data.instances })
                .enter()
                .append("g")
                    .attr("name", function(d, i) { return "instance-" + (i + 1) })

        pattern_instances
            .selectAll("circle")
                .data(function(d) { return d })
                .enter()
                .append("circle")
                    .attr("cx", function (d) { return x(d[0]) })
                    .attr("cy", function (d) { return y(d[1]) })
                    .on("mouseover", hover_on_pattern)
                    .on("mouseout", hover_off_pattern)
                    .transition()
                    .duration(300)
                    .attr("r", PATTERN_CIRCLE_RADIUS)

        pattern_path_generator = d3.line()
            .x(d => x(d[0]))
            .y(d => y(d[1]))

        pattern_instances
            .append("path")
                .attr("d", function(d) { return pattern_path_generator(d) })
                .attr("stroke-width", 0)
                .attr("fill", "none")
                .on("mouseover", hover_on_pattern)
                .on("mouseout", hover_off_pattern)
                .transition()
                .duration(300)
                .attr("stroke-width", PATH_WIDTH)
    } else {
        pattern_group = svg.selectAll("." + pattern_data.name)

        pattern_group
            .selectAll("circle")
                .transition()
                .duration(300)
                .attr("r", 0)

        pattern_group
            .selectAll("path")
                .transition()
                .duration(300)
                .attr("stroke-width", 0)

        pattern_group
            .transition()
            .duration(300).remove()
    }
}

d3.selectAll(".pattern-checkbox")
    .on("change", update_pattern_vis)

// Functions to highlight pattern when mouse hovers over them
function hover_on_pattern() {
    parent_group = d3.select(this.parentNode)

    parent_group
        .selectAll("circle")
            .transition()
            .duration(200)
            .attr("r", PATTERN_CIRCLE_RADIUS * 1.7)

    parent_group
        .selectAll("path")
            .transition()
            .duration(200)
            .attr("stroke-width", PATH_WIDTH * 2)
}

function hover_off_pattern() {
    parent_group = d3.select(this.parentNode)

    parent_group
        .selectAll("circle")
            .transition()
            .duration(200)
            .attr("r", PATTERN_CIRCLE_RADIUS)

    parent_group
        .selectAll("path")
            .transition()
            .duration(200)
            .attr("stroke-width", PATH_WIDTH)
}



//// Main visualisation
// Set the constants, dimensions and margins of the graph
const last_onset = data.point_set[data.point_set.length - 1][0]
const max_midi_pitch = 127
var margin = {top: 10, right: 30, bottom: 50, left: 70},
    width = Math.round(last_onset / 7500000),
    height = 600 - margin.top - margin.bottom

// Append the svg object to the page
var svg = d3.select("#point_set_vis")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

// Add X axis
var x = d3.scaleLinear()
    .domain([0, last_onset])
    .range([0, width])

svg
    .append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))

// Add X axis label
svg
    .append("text")
        .attr("text-anchor", "start")
        .attr("x", 20)
        .attr("y", height + margin.top + 25)
        .text("Note onset")

// Add Y axis
var y = d3.scaleLinear()
    .domain([0, max_midi_pitch])
    .range([height, 0])

svg
    .append("g")
        .call(d3.axisLeft(y))

// Add Y axis label
svg
    .append("text")
        .attr("text-anchor", "middle")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 20)
        .attr("x", -height / 2)
        .text("MIDI pitch number")

// Add the circles of the whole point set
svg
    .append("g")
        .attr("id", "point_set_circles")
        .selectAll("dot")
            .data(data.point_set)
            .enter()
            .append("circle")
                .attr("cx", function (d) { return x(d[0]) })
                .attr("cy", function (d) { return y(d[1]) })
                .style("fill", "#006666")
                .transition()
                .duration(1000)
                .attr("r", CIRCLE_RADIUS)
