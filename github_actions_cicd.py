#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-17 03:54:00 +0100 (Mon, 17 Apr 2023)
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

GitHub Actions CI/CD

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from diagrams import Diagram, Cluster, Edge

from diagrams.onprem.client import User
from diagrams.onprem.ci import Jenkins, GithubActions
from diagrams.onprem.vcs import Git, Github
from diagrams.saas.chat import Slack
from diagrams.programming.language import Python
from diagrams.programming.flowchart import Document

graph_attr = {
    "splines": "spline",
}

# pylint: disable=W0104,W0106
with Diagram('GitHub Actions CI/CD',
             show=not bool(os.environ.get('CI', 0)),
             direction='LR',
             filename="github_actions_ci_cd",
             graph_attr=graph_attr,
             ):

    hari = User("Hari\nPythonista")
    you = User("You")
    giovanni = User("Giovanni")
    git = Git("Git")

    hari \
        >> Edge(label="crazy midnight - 4am coding") \
        >> Python("Python") \
        >> Edge(label="git commit") \
        >> git

    with Cluster("Github"):
        github = Github("Diagrams-as-Code\nrepo")
        readme = Document("README.md")
        git \
            >> Edge(label="git push") \
            >> github \
            >> Edge(label="trigger workflow") \
            >> GithubActions("GitHub Actions\nCI/CD\nGenerate Images\nworkflow") \
            >> Edge(label="git commit\n&&\ngit push\nnew / updated diagrams") \
            >> github \
            >> readme

    with Cluster("Banned by Giovanni"):
        with Cluster("Do Not Use"):
            Jenkins("Jenkins")

    slack = Slack("Slack")

    hari \
        >> Edge(label="Hey Guys,\nlook what I just did this weekend!") \
        >> slack \
        >> giovanni \
        >> Edge(label="Hari is doing his rain man thing again...") \
        >> slack \

    you >> readme
