#!/usr/bin/env python

import os
import re
import sys
import numpy
import json
import argparse
import subprocess

#########1. PROGRAM ARGUMENTS #############

#1.1 Create object for argument parsinng
parser = argparse.ArgumentParser(prog="cnv_analyzer",description="CN analyzer, calculates mean copy number at genes and builds set of stats by sample and population.")     

#1.2 Definition of input parameters
input_group = parser.add_argument_group('Inputs')
input_group.add_argument('--cn-list', dest="cn_list", metavar="cn-list", nargs="+", help='List of copy number files, one per sample.\
                                                                                    Each copy number file must be a bedgraph. chr start end copynumber_value')
input_group.add_argument('--genes', dest="gene_bed", metavar="gene_bed", help='Genes BED file')

output_group = parser.add_argument_group('Output')
output_group.add_argument('--dir-out', dest="dir_out", metavar="dir-out", help='Directory to store output results')


#1.3 Argument parsing
args = parser.parse_args()

#1.4 Argumet checking
if len(args.cn_list) < 1:
    print "Sorry!! No copy number fields found. Specify at least one using --cn-list argument"
    sys.exit()

if not args.gene_bed:
    print "Sorry!! No gene bed files was found. Specify it using --genes argument"
    sys.exit()

if not args.dir_out:
    print "Sorry!! No output directory found."
    sys.exit()

#1.5 Output directory existance, checking and creation
if not os.path.exists(args.dir_out):
    os.makedirs(args.dir_out)

#########2. CREATE CNV FILES PER GENE #####

#2.1 Per each copy number file and gene bed graph create a median cn file per gene
listCnGeneFiles = []

for cnFile in args.cn_list:
    cnGeneFile = args.dir_out + "/" + os.path.basename(cnFile) + ".genes.bed"
    listCnGeneFiles.append(cnGeneFile)
    command = ["bedtools","map","-a",args.gene_bed,"-b",cnFile,"-c","4","-o","median"]  
    process = subprocess.Popen(command,stdout=open(cnGeneFile, 'w'))
    if process.wait() != 0:
        raise ValueError("Error while running %s"%(' '.join(command)))

#Gene Copy Number Output
#geneChrom  geneStart  geneEnd geneFields(1)... geneFields(N)   median

#########3. PARSING ALL CNV FILES #####

#Structure to load in memory Per Genes
#geneChrom geneStart geneEnd geneName medianCNSample1 medianCNSample2 ..  medianCNSample3
# [  [geneChrom,geneStart,geneEnd,geneName, [medianCNSample1,...,medianCNSampleN], [medPop,stDevPop] ] ,..., [geneChrom,geneStart,geneEnd,geneName, [medianCNSample1,...,medianCNSampleN] ] [medPop,stDevPop]  ] 
# [  [    0    ,    1    ,   2   ,    3   , [      4-0      ,...,      4-N      ], [  5-0 ,   5-1  ] ] ,..., [    0    ,    1    ,   2   ,    3    ,[      4-0      ,...,      4-N      ] ] [  5-0  ,  5-1  ]  ]
# [  [                                            0                                                  ] ,..., [                                                        N                                     ]  ]

#Structure to load in memory per Sample
#sampleName,copynumberValueGene1,...,copynumberValueGeneN,medianValueCopyNumber,standardDeviationCopyNumber
# [  [sampleName1, [cnGene1,...,cnGeneN],[medianCNgenes,stDevCNgenes] ] ,..., [sampleNameN, [cnGene1,...,cnGeneN],[medianCNgenes,stDevCNgenes] ]
# [  [      0    , [  1-0  ,...,   1-N ],[       2-0   ,     2-N    ] ] ,..., [      0    , [  1-0  ,...,   1-N ],[       2-0   ,     2-N    ] ]
# [  [                                     0                          ] ,..., [                              N                               ] ]


genesCopyNumber = []
samplesCopyNumber = []
jsonDictionary = {}

#3.1. Load all gene regions
with open(args.gene_bed, "r") as gene_file:
    for line in gene_file:
        fields = re.split('\t',line.rstrip('\n'))
        newRegion = [fields[0],fields[1],fields[2],fields[3],[],[]]
        genesCopyNumber.append(newRegion)

#3.2. Load copy number values per each file
for geneCN in listCnGeneFiles:
  
    genes_sample_CN_0_file = open(args.dir_out + "/" + os.path.basename(geneCN) + ".cn0", 'w')
    genes_sample_CN_1_file = open(args.dir_out + "/" + os.path.basename(geneCN) + ".cn1", 'w')
    genes_sample_CN_2_file = open(args.dir_out + "/" + os.path.basename(geneCN) + ".cn2", 'w') 
    genes_sample_CN_3_file = open(args.dir_out + "/" + os.path.basename(geneCN) + ".cn3", 'w')


    #Array Initialization [sampleName1, [cnGene1,...,cnGeneN],[medianCNgenes,stDevCNgenes] ]
    samplesCopyNumber.append([os.path.basename(geneCN),[],[]])
    nameSample = os.path.basename(geneCN) + "_" + os.path.basename(args.gene_bed)
    jsonDictionary [nameSample] = {"cn0":0,"cn1":0,"cn2":0,"cn3":0,"total":0,"median":0,"stDev":0} 
    jsonCounts = [0,0,0,0]

    index = 0

    with open(geneCN, "r") as cnGene:
        for line in cnGene:
            fields = re.split('\t',line.rstrip('\n'))
            copy_number = 0.0
            if genesCopyNumber[index][0] == fields[0] and genesCopyNumber[index][1] == fields[1] and genesCopyNumber[index][2] == fields[2]:
                if fields[-1] != ".":   
                    copy_number =  float(fields[-1])
                    
                genesCopyNumber[index][4].append(copy_number)
            else:
               raise Exception("No correspondence between loaded gen regions and copy number fields. Loaded gene file %s , Loading CN gene file %s " %(args.gene_bed,geneCN))
            
            #3.2.1 file per sample copy number per genes (0,1,2,3)
            if float(copy_number) < 0.5:
                genes_sample_CN_0_file.write(line)
                jsonCounts [0] = jsonCounts [0] + 1
            elif float(copy_number) >= 0.5 and float(copy_number) < 1.5:
                genes_sample_CN_1_file.write(line)
                jsonCounts [1] = jsonCounts [1] + 1
            elif float(copy_number) >= 1.5 and float(copy_number) <= 2.5: 
                genes_sample_CN_2_file.write(line)
                jsonCounts [2] = jsonCounts [2] + 1
            elif float(copy_number) > 2.5:   
                genes_sample_CN_3_file.write(line)
                jsonCounts [3] = jsonCounts [3] + 1
           
            index = index + 1

    genes_sample_CN_0_file.close()
    genes_sample_CN_1_file.close()
    genes_sample_CN_2_file.close()
    genes_sample_CN_3_file.close()

    #Statistics update
    jsonDictionary [nameSample]["cn0"] = jsonCounts [0]
    jsonDictionary [nameSample]["cn1"] = jsonCounts [1]
    jsonDictionary [nameSample]["cn2"] = jsonCounts [2]
    jsonDictionary [nameSample]["cn3"] = jsonCounts [3]
    jsonDictionary [nameSample]["total"] = jsonCounts [0] + jsonCounts [1] + jsonCounts [2] + jsonCounts [3]


#3.3 Statistics per population
genes_population_CN_0_file = open(args.dir_out + "/" + os.path.basename(args.gene_bed) + ".cn0.population.variability.bed", 'w')
genes_population_CN_1_file = open(args.dir_out + "/" + os.path.basename(args.gene_bed) + ".cn1.population.variability.bed", 'w')
genes_population_CN_2_file = open(args.dir_out + "/" + os.path.basename(args.gene_bed) + ".cn2.population.variability.bed", 'w') 
genes_population_CN_3_file = open(args.dir_out + "/" + os.path.basename(args.gene_bed) + ".cn3.population.variability.bed", 'w')

population_stats = [0,0,0,0]

#3.4 Process loaded data and calculates stats
for geneRegion in genesCopyNumber:
    #3.4.1 Get array numpy
    geneRegionsCnArray = numpy.array(geneRegion[4])
    #3.4.1 Get median
    median = numpy.median(geneRegionsCnArray)
    #3.4.2 Get StDeviation
    stDev = numpy.std(geneRegionsCnArray)
    #3.4.3 Print to file
    if median < 0.5:
        genes_population_CN_0_file.write(geneRegion[0] + "\t" + geneRegion[1] + "\t" + geneRegion[2] + "\t" + geneRegion[3] + "\t" + str(median) + "\t" + str(stDev) + "\n")
        population_stats [0] = population_stats[0] + 1
    elif median >= 0.5 and median < 1.5:
        genes_population_CN_1_file.write(geneRegion[0] + "\t" + geneRegion[1] + "\t" + geneRegion[2] + "\t" + geneRegion[3] + "\t" + str(median) + "\t" + str(stDev) + "\n")
        population_stats [1] = population_stats[1] + 1
    elif median >= 1.5 and median <= 2.5:
        genes_population_CN_2_file.write(geneRegion[0] + "\t" + geneRegion[1] + "\t" + geneRegion[2] + "\t" + geneRegion[3] + "\t" + str(median) + "\t" + str(stDev) + "\n")
        population_stats [2] = population_stats[2] + 1
    elif median > 2.5:
        genes_population_CN_3_file.write(geneRegion[0] + "\t" + geneRegion[1] + "\t" + geneRegion[2] + "\t" + geneRegion[3] + "\t" + str(median) + "\t" + str(stDev) + "\n")
        population_stats [3] = population_stats[3] + 1

    #3.4.4 Add StDev to sample
    indexSample = 0
    for sampleCn in samplesCopyNumber:
        sampleCn[1].append(float(geneRegion[4][indexSample]))
        indexSample = indexSample +1
    
    #3.4.5 Add StDev to Gene
    geneRegion[5] = [median,stDev]

#3.4.6 Close File Descriptors
genes_population_CN_0_file.close()
genes_population_CN_1_file.close()
genes_population_CN_2_file.close()
genes_population_CN_3_file.close()



#3.5 Calculate Standard Deviation and median per sample
sample_variability = open(args.dir_out + "/" + os.path.basename(args.gene_bed) + ".samples.variability.bed", 'w')

for sampleCn in samplesCopyNumber:
    cnArray = numpy.array(sampleCn[1])
    sampleCn[2] = [numpy.median(cnArray),numpy.std(cnArray)]
    sample_variability.write(sampleCn[0] + "\t" + str(sampleCn[2][0]) + "\t" + str(sampleCn[2][1]) + "\n")
    statsKey = sampleCn[0] + "_" + os.path.basename(args.gene_bed)
    jsonDictionary [statsKey]["median"] = sampleCn[2][0]
    jsonDictionary [statsKey]["stDev"] = sampleCn[2][1]


sample_variability.close()

#3.6 Create Dictionary Json Dictionary value
jsonDictionary ["population_genes"] = {"cn0":population_stats[0],"cn1":population_stats[1],"cn2":population_stats[2],"cn3":population_stats[3],\
                                       "total": population_stats[0] + population_stats[1] + population_stats[2] + population_stats[3]} 

with open(args.dir_out + "/" + os.path.basename(args.gene_bed) + ".stats.json", 'w') as of:
    json.dump(jsonDictionary, of, indent=2)



