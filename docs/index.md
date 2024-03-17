<style>

.inputs-3a86ea {

}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  /* margin: 4rem 0 8rem; */
  /* text-wrap: balance; */
  justify-content: center;
  padding: 
}

.hero p {
    text-align: justify;
}
.hero h1 {
  text-align: center;
  /* margin: 1rem 0; */
  max-width: 70vw;
  font-size: 35px;
  /* font-weight: 900; */
  font-weight: 750;
  line-height: 1.5;
  /* background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text; */
}

.hero h2 {
  margin: 0;
  max-width: 70vw;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

</style>


<div class="hero">
<h1>Differentiable Optimization of Similarity Scores Between Models and Brains</h1>

<h2>Nathan Cloos, Markus Siegel, Scott L. Brincat, Earl K. Miller, Christopher J. Cueva</h2>


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
  ["ultrametric", FileAttachment("data/ultrametric.csv").csv({typed: true})],
  ["siegel15-V4-var99", FileAttachment("data/siegel15-V4-var99.csv").csv({typed: true})],
  ["majajhong2015", FileAttachment("data/majajhong2015.csv").csv({typed: true})],
  ["FreemanZiemba2013", FileAttachment("data/FreemanZiemba2013.csv").csv({typed: true})],
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

<h3>Abstract</h3>
<p>
What metrics should guide the development of more realistic models of the brain? One proposal is to quantify the similarity between models and brains using methods such as linear regression, Centered Kernel Alignment (CKA), and Procrustes distance. To better understand the limitations of these similarity measures we analyze neural activity recorded in two experiments on nonhuman primates, and optimize synthetic datasets to become more similar to these neural recordings. How similar can these synthetic datasets be to neural activity while failing to encode task relevant variables? We find that some measures like linear regression and CKA, differ from Procrustes distance, and yield high similarity scores even when task relevant variables cannot be linearly decoded from the synthetic datasets. Synthetic datasets optimized to maximize similarity scores initially learn the first principal component of the target dataset, but Procrustes distance captures higher variance dimensions much earlier than methods like linear regression and CKA. When optimizing data towards neural activity we find the similarity scores at which principal components of this neural activity are learned, is well predicted by replacing neural activity with random datasets with matching distributions of singular values, suggesting new theoretical directions for studying these similarity measures.
</p>


</div>


