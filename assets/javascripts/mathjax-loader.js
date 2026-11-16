(function () {
  function hasMathContent(root) {
    if (!root) return false;

    const text = root.textContent || "";
    if (/\\\\\(|\\\\\)|\\\\\[|\\\\\]|\$\$/.test(text)) {
      return true;
    }

    return !!root.querySelector(
      [
        ".arithmatex",
        "script[type='math/tex']",
        "script[type='math/tex; mode=display']",
      ].join(",")
    );
  }

  function loadMathJax() {
    if (window.__khiopsMathJaxLoading) return;
    window.__khiopsMathJaxLoading = true;

    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }

  function maybeLoadMathJax() {
    var root = document.querySelector(".md-content") || document.body;
    if (hasMathContent(root)) {
      loadMathJax();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", maybeLoadMathJax, { once: true });
  } else {
    maybeLoadMathJax();
  }
})();
