#!/usr/bin/env python3

import sys
import os

if __name__ == "__main__":
    collection = sys.argv[1]
    input_path = sys.argv[2]

    # print(input_path)
    # for item in collection:
    # if item.endswith(".json"):
    # print(item)
    collection = collection.replace("[", "").replace("]", "")
    lst = collection.split(",")
    json_lst = [item.strip() for item in lst if item.endswith(".json")]
    print(list(set(json_lst)))
    # for item in set(lst):
    #     if item.endswith(".json"):
    #         print(item)
