#!/usr/bin/env python

import os
import sys
import requests
import xmltodict
import json
import datetime

downloadDir = "../data/datasets/SRA/"

date = datetime.datetime.now().strftime("%Y%m%d")

# Fetch BioProject from console with "-B" as identifier.
bioprojectIdentifierIndex = sys.argv.index("-B") if "-B" in sys.argv else None
bioproject = sys.argv[bioprojectIdentifierIndex+1] if bioprojectIdentifierIndex and ((len(sys.argv)-1) > bioprojectIdentifierIndex) else None

# Fetch platform from console with "-P" as identifier. "Illumina" or "Nanopore" only.
platformIdentifierIndex = sys.argv.index("-P") if "-P" in sys.argv else None
platform = sys.argv[platformIdentifierIndex+1] if platformIdentifierIndex and ((len(sys.argv)-1) > platformIdentifierIndex) and ((sys.argv[platformIdentifierIndex+1] == "Illumina") or (sys.argv[platformIdentifierIndex+1] == "Nanopore")) else None

if bioproject and platform:
    print("Error: Both BioProject (-B) and platform (-P) arguments provided. Only one argument needed.")
elif bioproject:
    params = {"save": "efetch", "db": "sra", "RetMax": "10000", "term": bioproject}

    print("Fetching...")
    request = xmltodict.parse(requests.get('http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi', params).text)
    
    fileName = date + "_" + bioproject + ".json"
    
    if not os.path.isdir(downloadDir):
        os.makedirs(downloadDir)

    with open(downloadDir + fileName, "w") as metadataFile:
        print("Writing to \"" + fileName + "\"...")
        json.dump(request, metadataFile, sort_keys=True, indent=4)
    print("Done.")
elif platform:
    platformTerm = "Illumina[Platform] AND \"paired\"[Layout]" if platform == "Illumina" else "Oxford Nanopore[Platform]" if platform == "Nanopore" else None

    searchTerm = "(txid2697049[Organism:noexp] AND \"public\"[Access]  AND " + platformTerm + ") NOT 0[Mbases]"
    params = {"save": "efetch", "db": "sra", "RetMax": "10000", "term": searchTerm}

    print("Fetching...")
    request = xmltodict.parse(requests.get('http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi', params).text)
    
    fileName = date + "_" + ("Illumina_paired" if platform == "Illumina" else "Nanopore") + ".json"
    
    if not os.path.isdir(downloadDir):
        os.makedirs(downloadDir)

    with open(downloadDir + fileName, "w") as metadataFile:
        print("Writing to \"" + fileName + "\"...")
        json.dump(request, metadataFile, sort_keys=True, indent=4)
    print("Done.")
else:
    print("None/Invalid BioProject (-B) or platform (-P) argument provided.\r\nNOTE: Only \"Illumina\" and \"Nanopore\" (case sensitive) platforms available.")
