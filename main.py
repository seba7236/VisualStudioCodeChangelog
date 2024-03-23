import json
import datetime
import os
import sys
from urllib.parse import unquote
import csv
import argparse


def convert_time(timestamp: int):
    return datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def parse_history(source, destination):
    jsonData = json.load(open(f"{source}/entries.json", "r"))
    originalFileName = jsonData["resource"].split("/")[-1]
    originalFilePath = jsonData["resource"].split("///")[-1]
    with open(f"{destination}/{originalFileName}_edits.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["original_path", "original_name", "temp_name", "saved_at"])
        for entry in jsonData["entries"]:
            csvwriter.writerow(
                [
                    f"{unquote(originalFilePath)}/{unquote(originalFileName)}",
                    unquote(originalFileName),
                    entry["id"],
                    convert_time(entry["timestamp"]),
                ]
            )


def main(source, destination):
    if source[-1] != "/":
        source = source+"/"
    if destination[-1] != "/":
        destination = destination + "/"
    for directory in os.listdir(source):
        parse_history(f"{source}{directory}", destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog="VSCode History Parser",
                        description="Parses the different versions of files in VSCode, for use with KAPE")
    parser.add_argument('-s','--src')
    parser.add_argument('-d','--dst')

    args = parser.parse_args()
    main(args.src, args.dst)
