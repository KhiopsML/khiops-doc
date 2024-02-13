---
hide:
  - toc
  - navigation
---

# Interactive Khiops Visualization Demo

Explore the capabilities of the Khiops Visualization Tool through three interactive analyses:

- **Single Table (Adult dataset)**: A straightforward supervised analysis demonstrating model performance and feature importance (and encoding) in a single-table context;
- **Single Table with Trees (Adult dataset)**: Enhances the first analysis by integrating trees;
- **Multi-Table (Accident dataset)**: Showcases a multi-table model, illustrating how our tool handles complex data structures and reveals key insights.

Click on the corresponding button to choose the case you want to explore:

<div id="visu-menu"></div>
<iframe name="visu-frame" id="visu-frame" src="/assets/khiops-visualization.html" style="width: 100%;height: 1024px;"></iframe>
<script>
	document.addEventListener("DOMContentLoaded", () =>
		visuMenu([
			{
				title: "Single Table",
				description: "Adult dataset",
				file: "/assets/mock/AdultReport.json"
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
			}
		])
	);
</script>