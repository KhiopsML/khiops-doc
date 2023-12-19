---
hide:
  - toc
  - navigation
---

# Khiops Visualization on the adult sample


<div id="visu-menu"></div>
<iframe name="visu-frame" id="visu-frame" src="/assets/khiops-visualization.html" style="width: 100%;height: 1024px;"></iframe>
<script>
	document.addEventListener("DOMContentLoaded", () =>
		visuMenu([
			{
				title: "Adult",
				description: "Adult file",
				file: "/assets/mock/AdultAllReports.json"
			},
			{
				title: "Crirteo",
				description: "Adult file",
				file: "/assets/mock/CrirteoAllReports.json"
			}
		])
	);
</script>