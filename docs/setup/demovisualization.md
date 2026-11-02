---
hide:
  - toc
  - navigation
---

# Interactive Khiops Visualization Demo

Explore the capabilities of the Khiops Visualization tool through five interactive analyses:

- **Single Table (Adult dataset)**: A straightforward supervised analysis demonstrating model performance and feature importance (and encoding) in a single-table context;
- **Single Table with Trees (Adult dataset)**: Enhances the first analysis by integrating trees;
- **Multi-Table (Accident dataset)**: Showcases a multi-table model, illustrating how our tool handles complex data structures and reveals key insights.
- **Variable x variable coclustering (Adult dataset)**: A co-clustering analysis to explore the dependance between two variables
- **Instances x Variables coclustering (Iris dataset)**: A co-clustering analysis exhibiting clusters of instances and clusters of parts of variable coming from any of the original variables

Click on the corresponding button to choose the case you want to explore:

<div id="visu-menu"></div>
<iframe name="visu-frame" id="visu-frame" src="/assets/khiops-visualization.html" style="width: 100%; height: calc(100vh - 200px); border: 2px solid black; padding: 10px; min-height: 1024px"></iframe>
<script>
	document.addEventListener("DOMContentLoaded", () =>
		visuMenu([
			{
				title: "Single Table",
				description: "Adult dataset",
				file: "/assets/mock/AdultCoclusteringReport.json"
			},
			{
				title: "Single Table with Trees",
				description: "Adult dataset",
				file: "/assets/mock/AdultWithTreesReport.json"
			},
			{
				title: "Multi-Table",
				description: "Accident dataset with three tables",
				file: "/assets/mock/AccidentReport.json"
			},
			{
				title: "Variable x variable coclustering",
				description: "Adult dataset with education and occupation variables",
				file: "/assets/mock/AdultCoclusteringReport.json"
			},
			{
				title: "Instances x variables coclustering",
				description: "Iris dataset with its five inner variables",
				file: "/assets/mock/IrisIVCoclusteringReport.json"
			}
		])
	);
</script>
