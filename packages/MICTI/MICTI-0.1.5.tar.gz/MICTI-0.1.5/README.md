MICTI- Marker gene Identification for Cell Type Identity
========================================================

Recent advances in single-cell gene expression profiling technology have revolutionized the understanding of molecular processes underlying developmental cell and tissue differentiation, enabling the discovery of novel cell types and molecular markers that characterize developmental trajectories.  Common approaches for identifying marker genes are based on pairwise statistical testing for differential gene expression between cell types in heterogeneous cell populations, which is challenging due to unequal sample sizes and variance between groups resulting in little statistical power and inflated type I errors. 

Overview
--------

We developed an alternative feature extraction method, *Marker gene Identification for Cell Type Identity* (**MICTI**), that encodes the cell-type specific expression information to each gene in every single cell. This approach identifies features (genes) that are cell-type specific for a given cell-type in heterogeneous cell population.


Installation
------------

To install the current release:

	pip install MICTI
	
How to use MICTI
----------------

Import MICTI:

	from MICTI import MARKER

Creating MICTI object for known cell-type cluster label:

	mictiObject=MARKER.MICTI(datamatrix, geneName, cellName, cluster_assignment=cell_type, k=None, th=0, ensembel=False, organisum="hsapiens")

2D visualisation with tSNE:

	mictiObject.get_Visualization(dim=2, method="tsne")

Get MICTI marker genes:

        cluster_1_markers=mictiObject.get_markers_by_Pvalues_and_Zscore(1, threshold_pvalue=.01,threshold_z_score=0)

Markers heatmap plots:

	mictiObject.heatMap()

Markers Radar plots:

	mictiObject.get_Radar_plot()

Gene Ontology enrichment analysis for cell-type marker genes in each of cell-type clusters

	enrechment_table=mictiObject.get_gene_list_over_representation_analysis(list(cluster_1_markers.index))
	enrechment_table #gene-list enrichment analysis result for the cell-type marker genes for cluster-1


Licence
-------

[MICTI LICENCE](./LICENSE)
