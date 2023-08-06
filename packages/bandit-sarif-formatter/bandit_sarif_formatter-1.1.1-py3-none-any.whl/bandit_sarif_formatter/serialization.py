# Copyright (c) Microsoft.  All Rights Reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import copy
import json


def generated_class_serializer(obj):
    if hasattr(obj, "__dict__"):
        dict = getattr(obj, "__dict__")
        dict = copy.deepcopy(dict)
        dict["test"] = 43
        return dict
    else:
        return str(obj)


def to_json(obj):
    return json.dumps(obj, indent=2, default=generated_class_serializer)
