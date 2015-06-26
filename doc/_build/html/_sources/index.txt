.. CNV Analyzer documentation master file, created by
   sphinx-quickstart on Tue Jun 16 15:37:03 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============
CNV Analyzer
============

----------------------------------------------------------------------------
Python script to cross copy number window values versus gene bed coordinates
----------------------------------------------------------------------------

CNV Analyzer uses `bedtools map`_ to extract copy number values from gene coordinates. `bedtools map`_ calculates the mean copy number value for those copy number windows overlapping gene
regions.


Statistics per gene and sample
------------------------------

Calculates gene copy number per each sample. Classifies each gene as copy number 0, 1, 2 and 3 or grater. Copy number values are estimated as float values, then a round is applied to 
classify it.


Statistics per Population
-------------------------

Calculates mean gene copy number from all gene copy number samples and gets its standard deviation.


Statistics per sample
---------------------

Calculates copy number on all genes of a given sample and its standard deviation.

Usage
-----

::

    cnv_analyzer --cn-list copy_number/*.bed --genes ensemble_genes.bed --dir-out directory_output

.. warning::

    --cn-list Files included in the file copy number list must represent a copy number file per sample. This copy number file must have four fields, chromosome start end copyNumberValue.

.. note::

    --genes parameter must be an annotation file in BED format.

------------
Output files
------------

Files generated:

+------------------------------------------------+------------------------------------------------------------------+
| File                                           | Description                                                      |
+================================================+==================================================================+
| sample.genes.bed                               | Per each sample copy number file. Outputs gene coordinates       |
|                                                | and its copy number value.                                       |
+------------------------------------------------+------------------------------------------------------------------+
| sample.genes.bed.cn0                           | Per each sample copy number file. Outputs gene coordinates       |
|                                                | and its copy number values and standard deviation for genes      |
|                                                | considered as copy number 0.                                     |
+------------------------------------------------+------------------------------------------------------------------+
| sample.genes.bed.cn1                           | Per each sample copy number file. Outputs gene coordinates       |
|                                                | and its copy number values and standard deviation for genes      |
|                                                | considered as copy number 1.                                     |
+------------------------------------------------+------------------------------------------------------------------+
| sample.genes.bed.cn2                           | Per each sample copy number file. Outputs gene coordinates       |
|                                                | and its copy number values and standard deviation for genes      |
|                                                | considered as copy number 2.                                     |
+------------------------------------------------+------------------------------------------------------------------+
| sample.genes.bed.cn3                           | Per each sample copy number file. Outputs gene coordinates       |
|                                                | and its copy number values and standard deviation for genes      |
|                                                | considered as copy number 3 or more.                             |
+------------------------------------------------+------------------------------------------------------------------+
| geneDatabase.cn0.population.variability.bed    | Copy number and Standard Deviation for all genes per population. | 
|                                                | The copy number is the median value from all samples.            |
|                                                | Genes considered as copy number 0.                               |
+------------------------------------------------+------------------------------------------------------------------+
| geneDatabase.cn1.population.variability.bed    | Copy number and Standard Deviation for all genes per population. | 
|                                                | The copy number is the median value from all samples.            |
|                                                | Genes considered as copy number 1.                               |
+------------------------------------------------+------------------------------------------------------------------+
| geneDatabase.cn2.population.variability.bed    | Copy number and Standard Deviation for all genes per population. | 
|                                                | The copy number is the median value from all samples.            |
|                                                | Genes considered as copy number 2.                               |
+------------------------------------------------+------------------------------------------------------------------+
| geneDatabase.cn3.population.variability.bed    | Copy number and Standard Deviation for all genes per population. | 
|                                                | The copy number is the median value from all samples.            |
|                                                | Genes considered as copy number 3 or more.                       |
+------------------------------------------------+------------------------------------------------------------------+
| geneDatabase.samples.variability.bed           | For all samples, median copy number value and standard deviation |
|                                                | in gene regions.                                                 |
+------------------------------------------------+------------------------------------------------------------------+
| geneDatabase.stats.json                        | JSON file of statistics per each sample and population.          |
|                                                |                                                                  |
|                                                | Number of genes copy number 0.                                   |
|                                                |                                                                  |
|                                                | Number of genes copy number 1.                                   |
|                                                |                                                                  |
|                                                | Number of genes copy number 2.                                   |
|                                                |                                                                  |
|                                                | Number of genes copy number 3 or more.                           |
|                                                |                                                                  |
|                                                | Median Copy Number value in genes.                               |
|                                                |                                                                  |
|                                                | Standard Deviation value in genes.                               |
|                                                |                                                                  |
+------------------------------------------------+------------------------------------------------------------------+

 

.. _bedtools map: http://bedtools.readthedocs.org/en/latest/content/tools/map.html


---------------
Important Notes
---------------

cnv_analyzer script uses Bedtools to perform some of the calculations. You must Install the package in your system to run
cnv_analyzer script.

Get last version from: `http://bedtools.readthedocs.org/en/latest/`_

.. _http://bedtools.readthedocs.org/en/latest/: http://bedtools.readthedocs.org/en/latest/





