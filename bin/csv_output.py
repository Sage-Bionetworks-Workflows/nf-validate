#!/usr/bin/env python3

import sys
import os
import csv
import json


def clean_json_list(json_list: str) -> list:
    """
    Cleans comma-separated string of JSON file paths and produces python list

    Args:
        json_list (str): comma-separated string with JSON file paths generated from nextflow channels

    Returns:
        list: python list of JSON file paths with validation test results
    """
    lst = json_list.replace("[", "").replace("]", "").split(",")
    final_list = [item.strip() for item in lst if item.endswith(".json")]
    final_list = list(set(final_list))
    return final_list


def generate_output_dict(input: str) -> dict:
    """
    creates teamplate output_dict from input csv file and including other necessary fields

    Args:
        input (str): file path for input csv file

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
                        "required_tests": "",  # placeholder for ome.tiff until we have required_tests from input
                        "is_valid": "",
                        "passed_tests": "",
                        "failed_tests": "",
                        "skipped_tests": "",
                    }
                }
            )
    return output_dict


def update_output_dict(final_list: list, output_dict: dict) -> dict:
    """
    updates output dict with validation results from all JSON files

    Args:
        final_list(list): clean list of JSON validation files
        output_dict (dict): output_dict generated to contain input.csv data and test result data

    Returns:
        dict: updated output_dict with validation test results
    """
    for item in final_list:
        # read validation data from json
        with open(item, "r") as file:
            data = json.load(file)
            # save reused variables
            syn_id = data["input"]["synapse_id"]
            test_name = data["test"]["name"]
            # set version number in output_dict
            output_dict[syn_id]["version_number"] = data["input"]["version_number"]
            # add tests to required_tests
            output_dict[syn_id]["required_tests"] += test_name + ";"
            # add tests to passed_tests or failed_tests
            if data["test"]["status"] == "pass":
                output_dict[syn_id]["passed_tests"] += test_name + ";"
            else:
                output_dict[syn_id]["failed_tests"] += test_name + ";"
            # set is_valid
            if (
                output_dict[syn_id]["passed_tests"]
                == output_dict[syn_id]["required_tests"]
            ):  # will there be tests run that are not required?
                output_dict[syn_id]["is_valid"] = True
            else:
                output_dict[syn_id]["is_valid"] = False
    return output_dict


def convert_output_dict(output_dict: dict) -> list:
    """
    converts output_dict to list of dicts to prepare for csv export

    Args:
        output_dict (dict): final output_dict with all input data and validation test results

    Returns:
        list: list of dictionaries containing all data needed for output csv file
    """
    output_list = []
    for k, v in output_dict.items():
        output_list.append(v)
    return output_list


def export_validation_results_csv(output_list: list):
    """
    exports output_list to csv file

    Args:
        output_list (list): list of dictionaries containing all data needed for output csv file
    """
    keys = output_list[0].keys()
    with open("validation_results.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_list)


if __name__ == "__main__":
    json_list = sys.argv[1]
    input = sys.argv[2]
    # clean up json_list
    final_list = clean_json_list(json_list)
    # create output dict from input csv (with only csv package - available in base python)
    output_dict = generate_output_dict(input)
    # update output_dict with validation test results
    output_dict = update_output_dict(final_list, output_dict)
    # convert output_dict to list of dicts
    output_list = convert_output_dict(output_dict)
    # write output_list to csv
    export_validation_results_csv(output_list)
