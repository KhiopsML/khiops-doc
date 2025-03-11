#  Technical limits

In order to be responsive on very large files, some display limitations are taken into account in Khiops Covisualization:

  - The khcj file size should not exceed 400 Mo.

  - The “composition” view displays the first 1 000 items. However the “copy data” feature allows to copy the first 100 000 values.

  - Khiops Covisualization evaluates the available memory and displays the coocurence matrix only if there is enough available memory.

  - There are slight occasional problems of automatic refreshment for large matrices. In this case you can easily refresh the matrix by switching the axis representation (Cf. 4.8.2. Axis representation).

If the khcj file is too big to be visualized in Khiops Covisualization, you can simplify the coclustering with Khiops Coclustering (see the Khiops Coclustering Guide section 3).