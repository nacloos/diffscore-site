```js
import * as d3 from "npm:d3";
```


<style>

.content {
  display: flex;
  flex-direction: column;
  /* Align items to the left */
  align-items: flex-start;
  font-family: var(--sans-serif);
  /* Center the content horizontally */
  margin-left: auto;
  margin-right: auto;
  /* Set a maximum width for the content */
  max-width: 950px; 
}

.content p, .content h3, .content h2, .content h1 {
  max-width: none;
  margin-top: 10px;
  margin-bottom: 20px;
}

.content p {
  text-align: justify;
}

.content .title, .content .authors {
  max-width: none;
  margin-right: auto;
  margin-left: auto;
  text-align: center;
}

.content .authors {
  margin-top: 10px;
  font-style: normal;
  /* text color dark grey */
  color: #666;
}

.content .observablehq--block {
  margin: auto;
}
.content #cell-c9425610 {
  max-width: 1000px;
  margin: auto;
  text-align: center;
}

.content .github-link {
  margin-top: 20px;
  text-align: center;
  margin: auto;
}

.content .github-link a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5; /* Light color background */
  color: #333;
  padding: 8px 12px;
  border-radius: 5px;
  text-decoration: none;
  font-size: 16px;
  border: 1px solid #ccc; /* Optional: adds a subtle border */
}

.content .github-link a:hover {
  background-color: #e9e9e9;
}

.content .github-link img {
  margin-right: 8px;
}

.content hr {
  border: 0;
  height: 1px;
  background-color: #ccc; /* Or any color you prefer */
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>


<div class="content">
<h1 class="title">Differentiable Optimization of Similarity Scores Between Models and Brains</h1>

<h2 class="authors">Nathan Cloos, Markus Siegel, Scott L. Brincat, Earl K. Miller, Guangyu Robert Yang, Christopher J. Cueva</h2>


<div class="github-link">
  <a href="https://github.com/nacloos/diffscore" target="_blank">
    <img src="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/256/github-icon.png" alt="GitHub" width="20">
    Code
  </a>
</div>



- [High scores failing to encoding task variables?](#high-scores-failing-to-encoding-task-variables)
- [Abstract](#abstract)
- [Similarity Repository](#similarity-repository)

## High scores failing to encoding task variables?

<hr>


```js
// TODO: not working
// const datasetScores = {
//   "ultrametric": FileAttachment("data/ultrametric.csv").csv({typed: true}),
//   "siegel15-V4-var99": FileAttachment("data/siegel15-V4-var99.csv").csv({typed: true}),
//   "MajajHong2015": FileAttachment("data/majajhong2015.csv").csv({typed: true}),
// };
// const datasetIds = Object.keys(datasetScores);

// const datasets = [
//   {id: "ultrametric", name: "Ultrametric", data: FileAttachment("data/ultrametric.csv").csv({typed: true})},
//   {id: "siegel15-V4-var99", name: "Siegel15 V4 Var99", data: FileAttachment("data/siegel15-V4-var99.csv").csv({typed: true})},
//   {id: "majajhong2015", name: "MajajHong2015", data: FileAttachment("data/majajhong2015.csv").csv({typed: true})},
//   {id: "FreemanZiemba2013", name: "FreemanZiemba2013", data: FileAttachment("data/FreemanZiemba2013.csv").csv({typed: true})},
// ]
// const datasetIds = datasets.map(d => d.id);

const datasets = new Map([
  ["Ultrametric", FileAttachment("data/ultrametric.csv").csv({typed: true})],
//  ["siegel15-V4-var99", FileAttachment("data/siegel15-V4-var99.csv").csv({typed: true})],
  ["MajajHong2015", FileAttachment("data/MajajHong2015.csv").csv({typed: true})],
  ["FreemanZiemba2013", FileAttachment("data/FreemanZiemba2013.csv").csv({typed: true})],
  ["Hatsopoulos2007", FileAttachment("data/Hatsopoulos2007.csv").csv({typed: true})],
  ["Mante2013", FileAttachment("data/Mante2013.csv").csv({typed: true})],
]);
const datasetIds = Array.from(datasets.keys());
```

```js
const selectedData = view(Inputs.select(datasets, {label: "Dataset"}))
```

```js
const defaultMeasures = ["cka", "procrustes-angular-score"]
// const measures = scores.map(d => d.measure).filter((v, i, a) => a.indexOf(v) === i);
const measures = selectedData.map(d => d.measure).filter((v, i, a) => a.indexOf(v) === i);
const selectedMeasures = view(Inputs.checkbox(measures, {label: "Measures", value: defaultMeasures}));
```

```js
// const scores = datasetScores.ultrametric;
// const filteredScores = scores.filter(d => selectedMeasures.includes(d.measure));
const filteredScores = selectedData.filter(d => selectedMeasures.includes(d.measure));
const plotScores = Plot.plot({
  color: {legend: true},
  marks: [
    Plot.line(
      filteredScores, 
      {
        x: "score",
        y: "decoding_accuracy",
        stroke: "measure",
        tip: true,
        strokeWidth: 3
    })
  ],
  style: {
    fontSize: "12px",
  }
})
display(plotScores);
```

## Abstract

<p>
What metrics should guide the development of more realistic models of the brain? One proposal is to quantify the similarity between models and brains using methods such as linear regression, Centered Kernel Alignment (CKA), and Procrustes distance. To better understand the limitations of these similarity measures we analyze neural activity recorded in two experiments on nonhuman primates, and optimize synthetic datasets to become more similar to these neural recordings. How similar can these synthetic datasets be to neural activity while failing to encode task relevant variables? We find that some measures like linear regression and CKA, differ from Procrustes distance, and yield high similarity scores even when task relevant variables cannot be linearly decoded from the synthetic datasets. Synthetic datasets optimized to maximize similarity scores initially learn the first principal component of the target dataset, but Procrustes distance captures higher variance dimensions much earlier than methods like linear regression and CKA.</p>


TODO: create one large gif so that they are sync?
<div style="">
  <img src="./data/animations/cka.gif" width=200 />
  <img src="./data/animations/ridge.gif" width=200 />
  <img src="./data/animations/procrustes-angular-score.gif" width=200 />
</div>


## Similarity Repository

```js
const measureCards = FileAttachment("data/cards/measures.csv").csv({typed: true});
```

```js
view(Inputs.table(measureCards));
```


```js
// https://d3-graph-gallery.com/graph/heatmap_style.html

const width = 200;
const height = 200;
const color = d3.scaleOrdinal(d3.schemeObservable10);

// append the svg object to the body of the page
// const svg = d3.create("svg")
//   .attr("width", width + margin.left + margin.right)
//   .attr("height", height + margin.top + margin.bottom)
// .append("g")
//   .attr("transform", `translate(${margin.left}, ${margin.top})`);

const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width+20, height+50])
    // .attr("style", "max-width: 100%; height: auto;");

//Read the data
d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv").then(function(data) {

  // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
  const myGroups = Array.from(new Set(data.map(d => d.group)))
  const myVars = Array.from(new Set(data.map(d => d.variable)))

  // Build X scales and axis:
  const x = d3.scaleBand()
    .range([ 0, width ])
    .domain(myGroups)
    .padding(0.05);
  svg.append("g")
    .style("font-size", 15)
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x).tickSize(0))
    .select(".domain").remove()

  // Build Y scales and axis:
  const y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
    .padding(0.05);
  svg.append("g")
    .style("font-size", 15)
    .call(d3.axisLeft(y).tickSize(0))
    .select(".domain").remove()

  // Build color scale
  const myColor = d3.scaleSequential()
    .interpolator(d3.interpolateInferno)
    .domain([1,100])

  // create a tooltip
  const tooltip = d3.select("#my_dataviz")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  // Three function that change the tooltip when user hover / move / leave a cell
  const mouseover = function(event,d) {
    tooltip
      .style("opacity", 1)
    d3.select(this)
      .style("stroke", "black")
      .style("opacity", 1)
  }
  const mousemove = function(event,d) {
    tooltip
      .html("The exact value of<br>this cell is: " + d.value)
      .style("left", (event.x)/2 + "px")
      .style("top", (event.y)/2 + "px")
  }
  const mouseleave = function(event,d) {
    tooltip
      .style("opacity", 0)
    d3.select(this)
      .style("stroke", "none")
      .style("opacity", 0.8)
  }

  // add the squares
  svg.selectAll()
    .data(data, function(d) {return d.group+':'+d.variable;})
    .join("rect")
      .attr("x", function(d) { return x(d.group) })
      .attr("y", function(d) { return y(d.variable) })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return myColor(d.value)} )
      .style("stroke-width", 4)
      .style("stroke", "none")
      .style("opacity", 0.8)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)
})

// Add title to graph
svg.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .attr("text-anchor", "left")
        .style("font-size", "22px")
        .text("A d3.js heatmap");

// Add subtitle to graph
svg.append("text")
        .attr("x", 0)
        .attr("y", -20)
        .attr("text-anchor", "left")
        .style("font-size", "14px")
        .style("fill", "grey")
        .style("max-width", 400)
        .text("A short description of the take-away message of this chart.");

display(svg.node())

```

</div>


