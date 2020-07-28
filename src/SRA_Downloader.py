#!/usr/bin/env python

import os
import sys
import json
import re
import requests
import shutil
import random
import datetime
from multiprocessing import Pool

downloadDir = "../data/Samples/regions/"
SRAMetadataDir = "../data/Datasets/SRA/"

countryTags = ["geo_loc_name", "geographic location (country and/or sea)", "country", "Country"]

# Fetch no. of processes from console with "-n" as identifier.
# Default: 1
samplesMultiprocessIdentifierIndex = sys.argv.index("-n") if "-n" in sys.argv else None
if samplesMultiprocessIdentifierIndex:
    if ((len(sys.argv)-1) > samplesMultiprocessIdentifierIndex) and sys.argv[samplesMultiprocessIdentifierIndex+1].isdigit():
        samplesMultiprocess = int(sys.argv[samplesMultiprocessIdentifierIndex+1])
    else:
        print("Invalid value for argument \"-n\".")
        sys.exit()
else:
    samplesMultiprocess = 1

# Fetch region from console with "-R" as identifier.
regionIdentifierIndex = sys.argv.index("-R") if "-R" in sys.argv else None
region = sys.argv[regionIdentifierIndex+1] if regionIdentifierIndex and ((len(sys.argv)-1) > regionIdentifierIndex) else None

# Fetch platform from console with "-P" as identifier. "Illumina" or "Nanopore" only.
platformIdentifierIndex = sys.argv.index("-P") if "-P" in sys.argv else None
platform = sys.argv[platformIdentifierIndex+1] if platformIdentifierIndex and ((len(sys.argv)-1) > platformIdentifierIndex) and ((sys.argv[platformIdentifierIndex+1] == "Illumina") or (sys.argv[platformIdentifierIndex+1] == "Nanopore")) else None

def downloadSample(i):
    exp = SRAMetadata["EXPERIMENT_PACKAGE_SET"]["EXPERIMENT_PACKAGE"][i]

    SRXID = exp["EXPERIMENT"]["@accession"]
    SRRID = exp["RUN_SET"]["RUN"]["@accession"]

    if not os.path.isdir(regionDir + SRXID):
        os.mkdir(regionDir + SRXID)

        try:
            if "@semantic_name" not in exp["RUN_SET"]["RUN"]["SRAFiles"]["SRAFile"]:
                for SRAFile in exp["RUN_SET"]["RUN"]["SRAFiles"]["SRAFile"]:
                    if SRAFile["@semantic_name"] == "run":
                        print("Downloading: " + SRXID + " " + str(round((int(SRAFile["@size"])/(1024*1024)),2)) + " MB")

                        with requests.get(SRAFile["@url"], stream=True) as fileStream:
                            with open(regionDir + SRXID + "/" + SRRID, "wb") as file:
                                shutil.copyfileobj(fileStream.raw, file)

            elif exp["RUN_SET"]["RUN"]["SRAFiles"]["SRAFile"]["@semantic_name"] == "run":
                print("Downloading: " + SRXID + " " + str(round((int(exp["RUN_SET"]["RUN"]["SRAFiles"]["SRAFile"]["@size"])/(1024*1024)),2)) + " MB")

                with requests.get(exp["RUN_SET"]["RUN"]["SRAFiles"]["SRAFile"]["@url"], stream=True) as fileStream:
                    with open(regionDir + SRXID + "/" + SRRID, "wb") as file:
                        shutil.copyfileobj(fileStream.raw, file)

            print("Downloaded: " + SRXID)
        except Exception as e:
            print(e)
    else:
        print(SRXID + " already exists. Skipping...")

if __name__ == "__main__":
    if region and platform:
        expList = []
        regionDir = downloadDir + region.replace(" ", "-") + "/"

        SRAMetadataFiles = [f for f in os.listdir(SRAMetadataDir) if os.path.isfile(SRAMetadataDir + f) and f.endswith(("Illumina_paired" if platform == "Illumina" else "Nanopore") + ".json")]
        
        if len(SRAMetadataFiles) != 0:
            # Fetch latest SRA Metadata file.
            SRAMetadataFile = max(list(map(lambda x: datetime.datetime.strptime(x.split("_")[0], "%d%m%Y"), SRAMetadataFiles))).strftime("%d%m%Y") + "_" + ("Illumina_paired" if platform == "Illumina" else "Nanopore") + ".json"
            print("Using " + SRAMetadataFile)

            SRAMetadata = json.load(open(SRAMetadataDir + SRAMetadataFile, "r"))

            for i in range(0,len(SRAMetadata["EXPERIMENT_PACKAGE_SET"]["EXPERIMENT_PACKAGE"])):
                exp = SRAMetadata["EXPERIMENT_PACKAGE_SET"]["EXPERIMENT_PACKAGE"][i]

                for tag in exp["SAMPLE"]["SAMPLE_ATTRIBUTES"]["SAMPLE_ATTRIBUTE"]:
                    if tag["TAG"] in countryTags:
                        if re.search(region, tag["VALUE"], re.IGNORECASE):
                            expList.append(i)

            if len(expList) > 0:
                print("Total samples for \"" + region + "\": " + str(len(expList)))

                if not os.path.isdir(downloadDir):
                    os.mkdir(downloadDir)

                if not os.path.isdir(regionDir):
                    os.mkdir(regionDir)

                # Sample file sizes tend to be similar in clusters (SRX IDs) due to group submissions.
                # Randomizing will assign those to different pools thus distributing similar loads.
                random.shuffle(expList)

                p = Pool(samplesMultiprocess)
                p.map(downloadSample, expList)
            else:
                print("No samples for \"" + region + "\".")
        else:
            print("No SRA metadata file for " + platform + " platform downloaded.")
    else:
        print("None/Invalid region (-R) or platform (-P) argument provided.\r\nNOTE: Only \"Illumina\" and \"Nanopore\" (case sensitive) platforms available.")
