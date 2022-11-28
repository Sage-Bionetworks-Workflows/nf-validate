#!/usr/bin/env python3

import sys
import csv
import json


def generate_output_dict(input: str) -> dict:
    """
    creates template output_dict from input csv file and including other necessary fields

    Args:
        input (str): file path to input csv file

    Returns:
        dict: dictionary containing data from input dict and new fields needed for output csv
    """
    output_dict = {}
    with open(input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            output_dict.update(
                {
                    row["synapse_id"]: {
                        "synapse_id": row["synapse_id"],
                        "file_type": row["file_type"],
                        "md5_checksum": row["md5_checksum"],
                        "version_number": "",
                        "required_tests": [],  # placeholder for ome.tiff until we have required_tests from input
                        "is_valid": "",
                        "passed_tests": [],
                        "failed_tests": [],
                        "skipped_tests": [],  # placeholder for future version with skipping
                    }
                }
            )
    return output_dict


def update_output_dict(json_list: list, output_dict: dict) -> dict:
    """
    updates output dict with validation results from all JSON files.
    compares passed_tests to required_tests to determine if file is valid.

    Args:
        json_list(list): list of JSON validation files
        output_dict (dict): output_dict generated to contain input.csv data and validation result data

    Returns:
        dict: updated output_dict with validation test results
    """
    # add validation results from JSON
    for item in json_list:
        # read validation data from json
        with open(item, "r") as file:
            data = json.load(file)
            # save reused variables
            syn_id = data["input"]["synapse_id"]
            test_name = data["test"]["name"]
            # set version number in output_dict
            output_dict[syn_id]["version_number"] = data["input"]["version_number"]
            # append required_tests
            output_dict[syn_id]["required_tests"].append(test_name)
            # add tests to passed_tests or failed_tests
            if data["test"]["status"] == "pass":
                output_dict[syn_id]["passed_tests"].append(test_name)
            else:
                output_dict[syn_id]["failed_tests"].append(test_name)

    # set is_valid
    for k, v in output_dict.items():
        v["is_valid"] = set(v["passed_tests"]) >= set(v["required_tests"])

    return output_dict


def export_validation_results_csv(output_dict: dict):
    """
    joins test lists in output dict to ;-separated strings.
    converts output_dict to list of dicts and exports output_list to csv file.

    Args:
        output_dict (dict): final output_dict with all input data and validation test results
    """
    # join lists
    for k in output_dict:
        output_dict[k]["required_tests"] = ";".join(
            sorted(output_dict[k]["required_tests"])
        )
        output_dict[k]["passed_tests"] = ";".join(
            sorted(output_dict[k]["passed_tests"])
        )
        output_dict[k]["failed_tests"] = ";".join(
            sorted(output_dict[k]["failed_tests"])
        )
        output_dict[k]["skipped_tests"] = ";".join(
            sorted(output_dict[k]["skipped_tests"])
        )

    # convert to list of dicts
    output_list = list(output_dict.values())

    # export to CSV
    keys = output_list[0].keys()
    with open("validation_results.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_list)


if __name__ == "__main__":
    input_csv = sys.argv[1]
    json_list = sys.argv[2:]

    # create output dict from input csv (with only csv package - available in base python)
    output_dict = generate_output_dict(input_csv)
    # update output_dict with validation test results
    output_dict = update_output_dict(json_list, output_dict)
    # write output_list to csv
    export_validation_results_csv(output_dict)
