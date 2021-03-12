"""Util functions."""

import glob
import json
import os
import os.path as osp
from collections import defaultdict
from typing import Dict, List, Tuple

from .typing import DictAny


def list_files(inputs: str) -> List[List[str]]:
    """List files names for a folder/nested folder."""
    files_list: List[List[str]] = []
    assert osp.isdir(inputs)
    sub_dirs = sorted(os.listdir(inputs))
    for sub_dir in sub_dirs:
        dir_path = osp.join(inputs, sub_dir)
        assert osp.isdir(dir_path)
        files = sorted(os.listdir(dir_path))
        files = [osp.join(dir_path, file_name) for file_name in files]
        files_list.append(files)
    return files_list


def read(inputs: str) -> List[List[DictAny]]:
    """Read annotations from file/files."""
    if osp.isdir(inputs):
        files = glob.glob(osp.join(inputs, "*.json"))
        outputs = [json.load(open(file)) for file in files]
    elif osp.isfile(inputs) and inputs.endswith("json"):
        outputs = json.load(open(inputs))
        if isinstance(outputs, dict):
            outputs = [[outputs]]
        elif isinstance(outputs, list) and isinstance(outputs[0], dict):
            outputs = [outputs]
    else:
        raise TypeError("Inputs must be a folder or a JSON file.")
    if "video_name" in outputs[0][0]:
        outputs = sorted(outputs, key=lambda x: str(x[0]["video_name"]))
    return outputs


def init(
    mode: str = "det", ignore_as_class: bool = False
) -> Tuple[DictAny, Dict[str, str], DictAny]:
    """Initialze the annotation dictionary."""
    coco: DictAny = defaultdict(list)
    coco["categories"] = [
        {"supercategory": "human", "id": 1, "name": "pedestrian"},
        {"supercategory": "human", "id": 2, "name": "rider"},
        {"supercategory": "vehicle", "id": 3, "name": "car"},
        {"supercategory": "vehicle", "id": 4, "name": "truck"},
        {"supercategory": "vehicle", "id": 5, "name": "bus"},
        {"supercategory": "vehicle", "id": 6, "name": "train"},
        {"supercategory": "bike", "id": 7, "name": "motorcycle"},
        {"supercategory": "bike", "id": 8, "name": "bicycle"},
    ]
    if mode == "det":
        coco["categories"] += [
            {
                "supercategory": "traffic light",
                "id": 9,
                "name": "traffic light",
            },
            {
                "supercategory": "traffic sign",
                "id": 10,
                "name": "traffic sign",
            },
        ]

    if ignore_as_class:
        coco["categories"].append(
            {
                "supercategory": "none",
                "id": len(coco["categories"]) + 1,
                "name": "ignored",
            }
        )

    # Mapping the ignored classes to standard classes.
    ignore_map = {
        "other person": "pedestrian",
        "other vehicle": "car",
        "trailer": "truck",
    }

    attr_id_dict: DictAny = {
        frame["name"]: frame["id"] for frame in coco["categories"]
    }
    return coco, ignore_map, attr_id_dict
