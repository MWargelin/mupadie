//// Data Structure after processing (for reference)
// {
//     "point_set": [[x1, y1], [x2, y2], ...],
//     "pattern_data": [
//         {
//             "meta": "Algorithm 0",
//             "patterns": [
//                 {
//                     "pattern_id": "algorithm-0-pattern-0",
//                     "normalised": [[i1x1minusx1, i1y1minusy1], [i1x2minusx1, i1y2minusy1], ...],
//                     "color": "#588c7e",
//                     "instances":[
//                         [[p1i1x1, p1i1y1], [p1i1x2, p1i1y2], ...],
//                         [[p1i2x1, p1i2y1], [p1i2x2, p1i2y2], ...],
//                         ...
//                     ]
//                 },
//                 ...
//             ]
//         },
//         ...
//     ]
// }



//// Constants, data processing and utility functions

var data = data

const CIRCLE_RADIUS = 3
const PATTERN_CIRCLE_RADIUS = 5
const PATH_WIDTH = 4
const CIRCLE_COLOR = "#006666"

const main_div = d3.select("#visualisation")

// Define first few colors of patterns manually to ensure
// contrasting colors. If there are more result sets, assign
// random colour
function pattern_color(i) {
    colors = [
        "#45548b",
        "#a14d51",
        "#89c14d",
        "#553a09"
    ]
    if (i < colors.length) {
        return colors[i]
    } else {
        return random_color()
    }
}

function random_color() {
    color1 = Math.floor(Math.random() * 210)
    color2 = Math.floor(Math.random() * 210)
    color3 = Math.floor(Math.random() * 210)
    return "rgb("+color1+", "+color2+", "+color3+")"
}

function normalise_pattern_instance(pattern_instance) {
    normalised = JSON.parse(JSON.stringify(pattern_instance))
    first_x = normalised[0][0]
    first_y = normalised[0][1]
    normalised.forEach(note => {
        note[0] -= first_x
        note[1] -= first_y
    });
    return normalised
}

// Turn patterns to dicts
// assign individual id for each pattern
// assign color for each result set
// and compute a normalised instance for pattern buttons
for (let i = 0; i < data.pattern_data.length; i++) {
    var result_dict = data.pattern_data[i];
    var algorithm_i = "algorithm-" + i
    var color = pattern_color(i)
    for (let j = 0; j < result_dict.patterns.length; j++) {
        var pattern_i = "pattern-" + j

        // If there's only one result set, use random colors
        // for each pattern. Otherwise one color per result set
        if (data.pattern_data.length === 1) {
            color = random_color()
        }

        result_dict.patterns[j] = {
            "pattern_id": algorithm_i + "-" + pattern_i,
            "normalised": normalise_pattern_instance(result_dict.patterns[j][0]),
            "instances": result_dict.patterns[j],
            "color": color
        }
    }
}



//// Main visualisation
// Set the constants, dimensions and margins of the graph
const max_midi_pitch = 127
var margin = {top: 10, right: 30, bottom: 50, left: 70},
    width = data.point_set.length * 15
    height = 600 - margin.top - margin.bottom

// Append the svg object to the page
var svg = main_div
    .append("div")
    .attr("class", "overflow-auto p-3 mb-3")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

// Add X axis
const last_onset = data.point_set[data.point_set.length - 1][0]
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

// Add the circles for the point set
svg
    .append("g")
        .selectAll("circle")
            .data(data.point_set)
            .enter()
            .append("circle")
                .attr("cx", function (d) { return x(d[0]) })
                .attr("cy", function (d) { return y(d[1]) })
                .style("fill", CIRCLE_COLOR)
                .transition()
                .duration(1000)
                .attr("r", CIRCLE_RADIUS)



//// Pattern selectors
// Set the dimensions and margins
var pattern_width = 155
var pattern_height = 100
var pattern_margin = {top: 10, right: 10, bottom: 25, left: 10}

// HTML tag structuring and styling
pattern_selectors = main_div
    .append("div")
    .selectAll("div")
        .data(data.pattern_data)
        .enter()
        .append("div")
            .attr("class", "p-2 mb-2")

// Result set descriptions
pattern_selectors
    .append("h4")
        .text(function(d, i) { return "Result set #" + (i+1) })
pattern_selectors
    .append("p")
        .text(function(d) { return d.meta })

// Create buttons for patterns
pattern_buttons = pattern_selectors
    .append("div")
        .attr("class", "overflow-scroll d-flex")
        .selectAll("svg")
            .data(function(d) { return d.patterns })
            .enter()
            .append("button")
                .attr("type", "button")
                .attr("class", "me-2 mb-2")
                .style("border-radius", "10px")
                .on("click", button_click)

// svg tags and groups that will contain the circles of patterns
pattern_groups = pattern_buttons
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
        .text(function (d, i) { return "Pattern " + (i+1) })

// Create scales for pattern circles in buttons
pattern_xs = []
pattern_ys = []
data.pattern_data.forEach(result_dict => {
    result_dict.patterns.forEach(pattern => {
        pattern.normalised.forEach(note => {
            pattern_xs.push(note[0])
            pattern_ys.push(note[1])
        });
    })
})
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
            .style("fill", CIRCLE_COLOR)
            .transition()
            .duration(1000)
            .attr("r", CIRCLE_RADIUS)

// Function to visualise patterns when a pattern button is clicked
function button_click() {
    button = d3.select(this)
    pattern_vis_id = button.datum().pattern_id + "-vis-group"
    pattern_vis_group = d3.select("#" + pattern_vis_id)
    if (pattern_vis_group.empty()) {
        // Pattern is not visualised -> Button was off, now on

        // Change button appearance
        color = button.datum().color

        button
            .transition()
            .duration(300)
            .style("background-color", color)
            .style("fill", "white")  // Pattern name font color
            .selectAll("circle")
                .style("fill", "white")

        // Visualise pattern
        pattern_group = svg
            .append("g")
                .attr("id", pattern_vis_id)
                .style("fill", color)
                .style("stroke", color)

        pattern_instances = pattern_group
            .selectAll(".pattern-instance")
                .data(button.datum().instances)
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
        // Pattern is visualised -> Button was on, now off

        // Change button appearance
        button
            .transition()
            .duration(300)
            .style("background-color", null)
            .style("fill", null)  // Pattern name font color
            .selectAll("circle")
                .style("fill", CIRCLE_COLOR)

        // Remove visualisation of pattern
        pattern_vis_group
            .selectAll("circle")
                .transition()
                .duration(300)
                .attr("r", 0)

        pattern_vis_group
            .selectAll("path")
                .transition()
                .duration(300)
                .attr("stroke-width", 0)

        pattern_vis_group
            .transition()
            .duration(300).remove()
    }
}

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
