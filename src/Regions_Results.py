#!/usr/bin/env python

from __future__ import division
import os
import sys
import json
import pandas as pd

coverageCutoff = 20
minorAlleleCutoff = 5
minorAlleleFreq = 0.005

outputDir = "../output/REDItools2/regions/"

# Fetch region from console with "-R" as identifier.
regionIdentifierIndex = sys.argv.index("-R") if "-R" in sys.argv else None
region = sys.argv[regionIdentifierIndex+1] if regionIdentifierIndex and ((len(sys.argv)-1) > regionIdentifierIndex) else None

if region:
    regionDir = outputDir + region.replace(" ", "-") + "/"
else:
    print("None/Invalid region (-R) argument provided.")
    sys.exit()

gisaid = pd.read_excel("../data/datasets/GISAID_Frequency.xlsx", sheet_name=region)
variationAnnotation = pd.read_excel("../data/datasets/BIGD_Variation_Annotation.xlsx", sheet_name="Sheet1")
    
cummFreq = pd.DataFrame(columns=["Position", "Reference", "Sub"], dtype=object)
cummCount = pd.DataFrame(columns=["Position", "Reference", "Sub"], dtype=object)

for sample in [i.split(".txt")[0] for i in os.listdir(regionDir) if i.endswith(".txt")]:
    rnaEdits = pd.read_csv(regionDir + sample + ".txt", sep="\t")
    temp = pd.DataFrame(columns=["Position", "Reference", "Coverage-q30", "A", "T", "G", "C", "Sub", "MA-Count", "MA-Freq"])

    for index, row in rnaEdits.iterrows():
        baseCount = dict(zip(["A", "C", "G", "T"], list(map(int, row["BaseCount[A,C,G,T]"].strip('][').split(', ')))))

        for sub in row["AllSubs"].split(' '):
            alleleCount = int(baseCount[sub.split(row["Reference"])[1]])
            alleleFreq = alleleCount/int(row["Coverage-q30"])
            
            if (int(row["Coverage-q30"]) >= coverageCutoff) and (alleleCount >= minorAlleleCutoff) and (alleleFreq >= minorAlleleFreq):
                temp = temp.append({"Position": row["Position"],
                                    "Reference": row["Reference"],
                                    "Coverage-q30": row["Coverage-q30"],
                                    "A": baseCount["A"],
                                    "T": baseCount["T"],
                                    "G": baseCount["G"],
                                    "C": baseCount["C"],
                                    "Sub": sub,
                                    "MA-Count": alleleCount,
                                    "MA-Freq": round(alleleFreq, 3)
                                }, ignore_index=True, sort=False)


    for index, row in temp.iterrows():
        if row["Position"] not in cummFreq["Position"].values:
            cummFreq = cummFreq.append(pd.DataFrame({"Position": row["Position"], "Reference": row["Reference"], "Sub": row["Sub"], sample: row["MA-Freq"]}, index=[0], dtype=object), ignore_index=True, sort=False)
        else:
            if row["Sub"] in cummFreq[cummFreq["Position"] == row["Position"]]["Sub"].values:
                cummFreq.loc[cummFreq[(cummFreq["Position"] == row["Position"]) & (cummFreq["Sub"] == row["Sub"])].index[0], sample] = row["MA-Freq"]
            else:
                cummFreq = cummFreq.append(pd.DataFrame({"Position": row["Position"], "Reference": row["Reference"], "Sub": row["Sub"], sample: row["MA-Freq"]}, index=[0], dtype=object), ignore_index=True, sort=False)
    
        if row["Position"] not in cummCount["Position"].values:
            cummCount = cummCount.append(pd.DataFrame({"Position": row["Position"], "Reference": row["Reference"], "Sub": row["Sub"], sample: row["MA-Count"]}, index=[0], dtype=object), ignore_index=True, sort=False)
        else:
            if row["Sub"] in cummCount[cummCount["Position"] == row["Position"]]["Sub"].values:
                cummCount.loc[cummCount[(cummCount["Position"] == row["Position"]) & (cummCount["Sub"] == row["Sub"])].index[0], sample] = row["MA-Count"]
            else:
                cummCount = cummCount.append(pd.DataFrame({"Position": row["Position"], "Reference": row["Reference"], "Sub": row["Sub"], sample: row["MA-Count"]}, index=[0], dtype=object), ignore_index=True, sort=False)

cummFreq = cummFreq.sort_values(by="Position")
cummFreq["Avg"] = cummFreq.iloc[:,3:].mean(axis=1).round(3) 
cummFreq["Count"] = cummFreq.iloc[:,3:len(cummFreq.columns)-1].fillna(0).astype(bool).sum(axis=1)
cummFreq["Count (>= 0.95)"] = (cummFreq.iloc[:,3:len(cummFreq.columns)-2] >= 0.95).sum(axis=1)
cummFreq["Editing Sub"] = cummFreq["Sub"]

for index, row in cummFreq.iterrows():
    nonRefBases = ["A", "T", "G", "C"]
    nonRefBases.remove(row["Reference"])
    gisaidSubs = None
    for i in nonRefBases:
        if gisaid.loc[gisaid["Pos"] == row["Position"], i].values[0] != 0:
            if gisaidSubs:
                gisaidSubs = gisaidSubs + ", " + row["Reference"] + i
            else:
                gisaidSubs = row["Reference"] + i
    cummFreq.loc[index, "GISAID Sub"] = gisaidSubs
    cummFreq.loc[index, "GISAID_A"] = gisaid.loc[gisaid["Pos"] == row["Position"], "A"].values[0]
    cummFreq.loc[index, "GISAID_T"] = gisaid.loc[gisaid["Pos"] == row["Position"], "T"].values[0]
    cummFreq.loc[index, "GISAID_G"] = gisaid.loc[gisaid["Pos"] == row["Position"], "G"].values[0]
    cummFreq.loc[index, "GISAID_C"] = gisaid.loc[gisaid["Pos"] == row["Position"], "C"].values[0]

for index, row in cummFreq.iterrows():
    if len(variationAnnotation[variationAnnotation["Genome position"] == row["Position"]]) != 0:
        cummFreq.loc[index, "Gene"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Gene name/Regions"].values[0]
        try:
            varCodons = None
            for i in variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Gene.Position.Codons"].values[0].split("; "):
                if varCodons:
                    varCodons = varCodons + "; " + i.split(":")[1]
                else:
                    varCodons = i.split(":")[1] 
            cummFreq.loc[index, "Variation Codons"] = varCodons
        except:
            pass
        cummFreq.loc[index, "Amino acids change"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Protein.Position.Amino acids change"].values[0]
        cummFreq.loc[index, "Annotation Type"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Annotation Type"].values[0]
        cummFreq.loc[index, "Calculated variant consequences"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Impact Ensembl Variation - Calculated variant consequences\">"].values[0]

print("Writing frequencies...")
cummFreq.to_csv(regionDir + "Frequencies.tsv", index=False, sep="\t")

cummCount = cummCount.sort_values(by="Position")
cummCount["Avg"] = cummCount.iloc[:,3:].mean(axis=1).round(2)
cummCount["Count"] = cummCount.iloc[:,3:len(cummCount.columns)-1].fillna(0).astype(bool).sum(axis=1)
cummCount["Editing Sub"] = cummCount["Sub"]

for index, row in cummCount.iterrows():
    nonRefBases = ["A", "T", "G", "C"]
    nonRefBases.remove(row["Reference"])
    gisaidSubs = None
    for i in nonRefBases:
        if gisaid.loc[gisaid["Pos"] == row["Position"], i].values[0] != 0:
            if gisaidSubs:
                gisaidSubs = gisaidSubs + ", " + row["Reference"] + i
            else:
                gisaidSubs = row["Reference"] + i
    cummCount.loc[index, "GISAID Sub"] = gisaidSubs
    cummCount.loc[index, "GISAID_A"] = gisaid.loc[gisaid["Pos"] == row["Position"], "A"].values[0]
    cummCount.loc[index, "GISAID_T"] = gisaid.loc[gisaid["Pos"] == row["Position"], "T"].values[0]
    cummCount.loc[index, "GISAID_G"] = gisaid.loc[gisaid["Pos"] == row["Position"], "G"].values[0]
    cummCount.loc[index, "GISAID_C"] = gisaid.loc[gisaid["Pos"] == row["Position"], "C"].values[0]

for index, row in cummCount.iterrows():
    if len(variationAnnotation[variationAnnotation["Genome position"] == row["Position"]]) != 0:
        cummCount.loc[index, "Gene"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Gene name/Regions"].values[0]
        try:
            varCodons = None
            for i in variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Gene.Position.Codons"].values[0].split("; "):
                if varCodons:
                    varCodons = varCodons + "; " + i.split(":")[1]
                else:
                    varCodons = i.split(":")[1] 
            cummCount.loc[index, "Variation Codons"] = varCodons
        except:
            pass
        cummCount.loc[index, "Amino acids change"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Protein.Position.Amino acids change"].values[0]
        cummCount.loc[index, "Annotation Type"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Annotation Type"].values[0]
        cummCount.loc[index, "Calculated variant consequences"] = variationAnnotation.loc[variationAnnotation["Genome position"] == row["Position"], "Impact Ensembl Variation - Calculated variant consequences\">"].values[0]

print("Writing counts...")
cummCount.to_csv(regionDir + "Counts.tsv", index=False, sep="\t")
