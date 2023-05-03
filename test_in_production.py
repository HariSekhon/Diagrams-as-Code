#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-17 00:08:14 +0100 (Mon, 17 Apr 2023)
#
#  https://github.com/HariSekhon/Diagrams-as-Code
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/HariSekhon
#

"""

Release Straight to Production

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from diagrams import Diagram, Edge

from diagrams.programming.flowchart import Action, Database, Decision, Delay, Document, InputOutput, MultipleDocuments
from diagrams.c4 import Container

graph_attr = {
    "splines": "spline",
}

# pylint: disable=W0104,W0106
with Diagram('Release Straight to Production!',
             show=not bool(os.environ.get('CI', 0)),
             direction='BT',
			 graph_attr=graph_attr
             ):
    prod = Action("Prod")
    for _ in range(1, 4, 1):
        Action("Dev") >> Edge(label=f"Feature {_}") >> prod
