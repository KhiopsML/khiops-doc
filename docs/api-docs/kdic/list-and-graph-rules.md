# List and graph rules

The `BuildList` and `BuildGraph` rules help transform raw data into linked lists and graphs. They enable efficient organization and analysis of relationships within your data.

## BuildList

```kdic-api-docs
Table(TargetDic) BuildList(Table(SourceDic) sourceTable 
                           :
                           Entity(SourceDic) Content, 
                           Entity(TargetDic) Prev, Entity(TargetDic) Next)
```

Creation of a target table from a source table, where each target instance is a list element, with a reference to the current source instance and links to the previous and next elements of the list

- The source table must be sorted according to user needs.

- The target dictionary must contain one variable of type Entity(SourceDir) containing the current source instance and two variables of type Entity(TargetDic), designated in the rule as Prev and Next, intended to hold references to the previous and next list elements.

- This allows adding new derived variables in the target dictionary that exploit the current instance values and those of its previous or next ones, or even several previous instances.

- The previous link of the first list element is missing, as is the next link of the last list element.

### Emulating the BuildDiffTable rule

This example demonstrates how to build a list of sales ordered by date and compute differences between successive sales, as with the [`BuildDiffTable`](../kdic/temporal-rules.md/#builddifftable) rule.

!!! example "Emulating the BuildDiffTable rule"
    
    
    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Numerical age;
      Categorical sex;
      Table(Sale) sales;
      Unused Table(Sale) sorted_sales = TableSort(sales, purchase_date);

      // Linked list built from the sorted sales
      Table(OrderedSale) list_sales = BuildList(sorted_sales : sale, prev_sale, next_sale);
    };
    
    Dictionary Sale (customer_id)
    {
      Categorical customer_id;
      Categorical product;
      Categorical sale_type;
      Numerical cost;
      Date purchase_date;
    };
    
    Dictionary OrderedSale
    {
      Entity(Sale) sale;             // Reference to current sale
      Entity(OrderedSale) prev_sale; // Link to previous sale element
      Entity(OrderedSale) next_sale; // Link to next sale element
    
      // Differences computed between two succesive elements of the list
      Unused Entity(Sale) previous_sale = GetEntity(prev_sale, sale);    // Access to previous sale
      Numerical diff_type = EQc(GetValueC(sale, sale_type), GetValueC(previous_sale, sale_type));
      Numerical diff_cost = Diff(GetValue(sale, cost), GetValue(previous_sale, cost));
      Numerical diff_date = DiffDate(GetValueD(sale, purchase_date), GetValueD(previous_sale, purchase_date));
    };
    ```

### Using a temporal window for smoothing purpose

This example illustrates how to use a list of measures to compute a smoothed value by considering neighboring elements within a temporal window.

!!! example
    
    ```kdic
    Root Dictionary Curve (id)
    {
      Categorical id;
      Table(Measure) measures;
      Unused Table(Measure) sorted_measures = TableSort(measures, t);

      // Linked list built from from the sorted measures
      Table(MeasureElement) list_measures = BuildList(sorted_measures:measure, prev, next);
    };
    
    Dictionary Measure (id)
    {
      Categorical id;
      Numerical t;
      Numerical x;
    };
    
    Dictionary MeasureElement
    {
      Entity(Measure) measure;      // Reference to current measure
      Entity(MeasureElement) prev;  // Link to previous element
      Entity(MeasureElement) next;  // Link to previous element

      // Access to neighboring list elements
      Entity(MeasureElement) prev_prev = GetEntity(prev, prev);
      Entity(MeasureElement) next_next = GetEntity(next, next);

      // Window of list measures around the current measure
      Table(Measure)  window = EntitySet(GetEntity(prev_prev, measure),
                                         GetEntity(prev, measure),
                                         measure,
                                         GetEntity(next, measure),
                                         GetEntity(next_next, measure));

      // Current time and value, with a smoothed version of the value        
      Numerical t = GetValue(measure, t);
      Numerical smoothed_x = TableMean(window, x);
    };
    ```

## BuildGraph

```kdic-api-docs
Entity(GraphDic) BuildGraph(Table(NodeDataDic) inputNodeTable,
                            Categorical nodeId,
                            Table(EdgeDataDic) inputEdgeTable,
                            Categorical node1Id, Categorical node2Id
                            :
                            Table(NodeDic) graphNodeTable,
                            Entity(NodeDataDic) nodeData,
                            Table(EdgeDic) nodeAdjacentEdges,
                            Table(EdgeDic) graphEdgeTable,
                            Entity(EdgeDataDic) edgeData,
                            Entity(NodeDic) edgeNode1,
                            Entity(NodeDic) edgeNode2)
```

Creation of an undirected graph from an input table of nodes and an output table of edges, where each input node has an identifier and each input edge has a pair of node identifiers.

The target dictionary GraphDic contains:

- A table of nodes, each with its node data and adjacent edges

- A list of edges, each with its edge data and source and target nodes

**Inputs:**

- Table(`NodeDataDic`) inputNodeTable : table of input nodes

    - Categorical nodeId : identifier of nodes within inputNodeTable

- Table(`EdgeDataDic`) inputEdgeTable : table of input edges

    - Categorical node1Id, node2Id : identifiers of node pairs associated with each edge in inputEdgeTable

**Outputs:**

- Table(`NodeDic`) graphNodeTable : table of graph nodes within the targe dictionary `GraphDic`

    - Entity(`NodeDataDic`) nodeData : stores source node data within each node

    - Table`EdgeDic`) nodeAdjacentEdges : list of edges adjacent to each node

- Table(`EdgeDic`) graphEdgeTable : table of graph edges within the targe dictionary `GraphDic`

    - Entity(`EdgeDataDic`) edgeData : stores source edge data within each edge

    - Entity(`NodeDic`) edgeNode1, edgeNode2 : references to the node entities connected by each edge

**Additional considerations:**

- Multigraphs are allowed, meaning multiple edges can connect the same pair of nodes.

- For directed graphs, the adjacent edges can be separated into incoming and outgoing edges using the TableSelection rule.

- Management of inconsistencies:

    - If multiple input nodes share the same identifier, only the first node is kept for building the graph node; others are ignored. This can be detected by comparing the number of input nodes with the number of unique graph nodes created, using the TableCount rule.

    - If input edges reference missing nodes, the corresponding graph edges are not created. This inconsistency can be identified again using the TableCount rule.

### Example with a directed weighted graph

This example demonstrates how to construct a directed, weighted graph from data files describing nodes and edges.

!!! example

    <img  src="/assets/images/graph_sample.png" ;></img>
    
    This network is stored in three files: one line in the networks file for the entire network, and one line each in the nodes and edges files for individual nodes and edges.
    

    | Networks.txt       | NetworkNodes.txt             | NetworkEdges.txt                                 |
    | -------------------|------------------------------| ------------------------------------------------ |
    | NetworkId, Name    | NetworkId, NodeId, NodeValue | NetworkId, SourceNodeId, TargetNodeId, EdgeValue |
    | Net1, First sample | Net1, N1, 1                  | Net1, N1, N1, 1                                  |
    | ...                | Net1, N2, 2                  | Net1, N2, N1, 2                                  |
    |                    | Net1, N3, 3                  | Net1, N3, N1, 0.5                                |
    |                    | Net1, N4, 4                  | Net1, N4, N1, 1                                  |
    |                    | ...                          | Net1, N4, N2, 0.2                                |
    |                    |                              | Net1, N4, N4, 4                                  |
    |                    |                              | ...                                              |
    
    The three files are described by dictionaries Network, NetworkNode and NetworkEdge.
    
    The `BuildGraph` rule allows to construct an in memory graph with nodes connected to their adjacents edges and edges connected to their source and target nodes, using the three dictionaries `Graph`, `Node` and `Edge`.
    
    The `TableSelection` rule is used in dictionary `Node` to select the incoming out outgoing edges from the adjacent edges, by comparing the current node id (in the scope of the node (cf. `.NodeId`)) with the source or target node id of the edges.

    ```kdic
    // Dictionary for networks nodes stored in a data table file
    Dictionary NetworkNode (NetworkId, NodeId)
    {
      Categorical NetworkId; // Identifier of the network
      Categorical NodeId;    // Unique node identifier within the network
      Numerical NodeValue;   // Node value
    };

    // Dictionary for network edges stored in a data table file
    Dictionary NetworkEdge (NetworkId, SourceNodeId, TargetNodeId)
    {
      Categorical NetworkId;    // Identifier of the network
      Categorical SourceNodeId; // Identifier of the source node of the edge
      Categorical TargetNodeId; // Identifier of the target node of the edge
      Numerical EdgeValue;      // Edge value
    };

    // Dictionary for networks stored in a data table file
    // An in-memory graph is built using the BuildGraph rule
    Root Dictionary Network (NetworkId)
    {
      Categorical NetworkId; // Identifier of the network
      Categorical Name;      // Name of the network
    
      // Network nodes and edges are unused here but will be used in graph construction
      Unused Table(NetworkNode) NetworkNodes;
      Unused Table(NetworkEdge) NetworkEdges;
    
      // Graph of the network built from the network nodes and edges tables
      Entity(Graph) GraphNetwork = BuildGraph(NetworkNodes, NodeId,
                                              NetworkEdges, SourceNodeId, TargetNodeId
                                              :
                                              Nodes, Data, AdjacentEdges,
                                              Edges, Data, SourceNode, TargetNode);
    };

    // Dictionary for in-memory nodes, built using the BuildGraph rule
    Dictionary Node
    {
      Entity(NetworkNode) Data;  // Network node data
      Table(Edge) AdjacentEdges; // Edges connected to this node
      Categorical NodeId = GetValueC(Data, NodeId); // Node id, retrieved from node data
    
      // Incoming edges obtained by selecting the adjacent edges having a target node Id equal to the current node Id
      Table(Edge) IncomingEdges = TableSelection(AdjacentEdges, EQc(.NodeId, GetValueC(TargetNode, NodeId)));
    
      // Outgoing edges obtained by selecting the adjacent edges having a source node Id equal to the current node Id
      Table(Edge) OutgoingEdges = TableSelection(AdjacentEdges, EQc(.NodeId,GetValueC(SourceNode, NodeId)));
    };

    // Dictionary for in-memory edges, built using the BuildGraph rule
    Dictionary Edge
    {
      Entity(NetworkEdge) Data; // Network edge data
      Entity(Node) SourceNode;  // Source node of the edge
      Entity(Node) TargetNode;  // Target node of the edge
    };

    // Dictionary for in-memory graphs, built using the BuildGraph rule
    Dictionary Graph
    {
      Table(Node) Nodes; // Nodes in the graph
      Table(Edge) Edges; // Edges in the graph
    };
    ```

### Datasets of molecules, with their atoms and bonds

This example demonstrates how to model molecular structures as graphs, with atoms as nodes and bonds as edges.    

!!! example
    
    ```kdic
    // Dictionary for atoms stored in a data table file
    Dictionary Atom (MoleculeId, AtomId)
    {
      Categorical MoleculeId; // Identifier for the molecule
      Categorical AtomId;     // Unique atom identifier within the molecule
      Categorical element;    // Element type (e.g., C, H, O)
      Numerical type;         // Atom type
      Numerical charge;       // Atom charge
    };

    // Dictionary for bonds stored in a data table file
    Dictionary Bond (MoleculeId, AtomId1, AtomId2)
    {
      Categorical MoleculeId; // Identifier for the molecule
      Categorical AtomId1;    // First atom in the bond
      Categorical AtomId2;    // Second atom in the bond
      Categorical bondtype;   // Type of bond
    };

    // Dictionary for molecules stored in a data table file
    // An in-memory graph is built using the BuildGraph rule
    Root Dictionary Molecule (MoleculeId)
    {
      Categorical MoleculeId; // Unique molecule identifier
      Categorical class;      // Molecule class/type
      Numerical lumo;         // LUMO energy
      Numerical logp;         // LogP value (hydrophobicity)

      // Atoms and bonds are unused here but will be exploited for graph construction
      Unused Table(Atom) Atoms;
      Unused Table(Bond) Bonds;

      // Graph of the molecule built from the atom and bond tables
      Entity(GraphMolecule) GraphMolecule = BuildGraph(Atoms, AtomId,
                                                       Bonds, AtomId1, AtomId2 :
                                                       Atoms, AtomData, AdjacentBonds,
                                                       Bonds, BondData, Atom1, Atom2);
    };

    // Dictionary for in-memory atoms, built using the BuildGraph rule
    Dictionary GraphAtom
    {
      Entity(Atom) AtomData;          // Atom source data
      Table(GraphBond) AdjacentBonds; // Bonds connected to this atom
    };

    // Dictionary for in-memory bonds, built using the BuildGraph rule
    Dictionary GraphBond
    {
      Entity(Bond) BondData;   // Bond source data
      Entity(GraphAtom) Atom1; // First atom entity
      Entity(GraphAtom) Atom2; // Second atom entity
    };

    // Dictionary for in-memory molecules, built using the BuildGraph rule
    Dictionary GraphMolecule
    {
      Table(GraphAtom) Atoms; // Atoms as nodes in the graph
      Table(GraphBond) Bonds; // Bonds as edges in the graph
    };
    ```    