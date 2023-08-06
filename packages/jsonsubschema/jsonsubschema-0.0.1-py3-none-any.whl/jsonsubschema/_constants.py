'''
Created on June 7, 2019
@author: Andrew Habib
'''

import operator
from functools import reduce


Jnumeric = set(["integer", "number"])

Jtypes = Jnumeric.union(["string", "boolean", "null", "array", "object"])

JtypesToKeywords = {
    "string": ["minLength", "maxLength", "pattern"],
    "number": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
    "integer": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
    "boolean": [],
    "null": [],
    "array": ["minItems", "maxItems", "items", "additionalItems", "uniqueItems"],
    "object": ["properties", "additionalProperties", "required", "minProperties", "maxProperties", "dependencies", "patternProperties"]
}

Jconnectors = set(["anyOf", "allOf", "oneOf", "not"])

Jcommonkw = Jconnectors.union(["enum", "type"])

Jmeta = set(["$schema", "$id", "$ref", "definitions", "title", "description"])

Jkeywords = Jcommonkw.union(Jtypes,
                            reduce(operator.add, JtypesToKeywords.values()))

JtypesToPyTypes = {"integer": int, "number": float, "string": str,
                   "boolean": bool, "null": type(None), "array": list, "object": dict}

PyTypesToJtypes = dict([(v, k) for k, v in JtypesToPyTypes.items()])
