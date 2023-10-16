#!/usr/bin/env python3
"""
A function that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """A function that returns the list of school having a specific topic"""
    result = mongo_collection.find({"topics": topic}, {"_id": 0, "name": 1})
