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
__version__ = '0.4.1'

import os
#import requests

from diagrams import Diagram, Cluster, Edge

# ============================================================================ #
# On-premise / Open Source resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/onprem
#

#from diagrams.onprem.client import User  # , Users
from diagrams.onprem.ci import Jenkins, GithubActions
from diagrams.onprem.vcs import Git, Github

# ============================================================================ #
# SaaS:
#
#   https://diagrams.mingrammer.com/docs/nodes/saas
#

from diagrams.saas.chat import Slack

# ============================================================================ #
#
# Programming - flowcharts, programming languages and frameworks
#
#   https://diagrams.mingrammer.com/docs/nodes/programming
#

from diagrams.programming.language import Python
from diagrams.programming.flowchart import Document

# ============================================================================ #
#
# Custom - for creating a custom object using a downloaded image
#
#   https://diagrams.mingrammer.com/docs/nodes/custom
#

from diagrams.custom import Custom

# ============================================================================ #

# pylint: disable=C0103
headers = {'user-agent': 'Mozilla/5.0'}
hari_icon = "hari.jpeg"
# rolling_eyes_url = "https://em-content.zobj.net/thumbs/240/apple/354/face-with-rolling-eyes_1f644.png"
rolling_eyes_icon = "rolling_eyes.png"

# r = requests.get(rolling_eyes_url, headers=headers)
# with open(rolling_eyes_icon, 'wb') as f:
#     f.write(r.content)

# r = requests.get(hari_url, headers=headers)
# with open(hari_icon, 'wb') as f:
#     f.write(r.content)

# ============================================================================ #

graph_attr = {
    "splines": "spline",
}

image_dir = 'images'

# pylint: disable=W0104,W0106
with Diagram('GitHub Actions CI/CD - Auto-(Re)Generate Diagrams',
             show=not bool(os.environ.get('CI', 0)),
             direction='LR',
             filename=os.path.join(image_dir, "github_actions_cicd"),
             graph_attr=graph_attr,
             ):

    #hari = User("Hari\nPythonista")
    hari = Custom("Hari\nPythonista", hari_icon)
    #giovanni = User("Giovanni")
    giovanni = Custom("Giovanni", rolling_eyes_icon)
    #ravi = User("Ravi")
    ravi = Custom("Ravi", "man-shrugging-medium-skin-tone.png")
    #you = User("You")
    you = Custom("You", "flushed-face.png")
    #users = Users("Users")
    git = Git("Git")

    hari \
        >> Edge(label="crazy midnight to 4am coding") \
        >> [
                # can't handle svg
                #Custom("D2", "d2_graphic.svg")
                #Custom("D2", "d2_logo.png")
                Custom("D2", "d2_graphic.png"),
                Python("Python")
           ] \
        >> Edge(label="git commit") \
        >> git

    with Cluster("GitHub"):
        github_repo = Github("Diagrams-as-Code\nGitHub repo")
        with Cluster("GitHub Actions\nCI/CD"):
            python_workflow = GithubActions("Generate Python\nImages workflow")
            d2_workflow = GithubActions("Generate D2\nImages workflow")
        readme = Document("README.md")
        git >> Edge(label="git push") >> github_repo
        github_repo >> Edge(label="*.py changes trigger workflow") >> python_workflow
        github_repo >> Edge(label="*.d2 changes trigger workflow") >> d2_workflow
        [python_workflow, d2_workflow] \
            >> Edge(label="git commit new / updated diagrams") \
            >> github_repo \
            >> readme

    with Cluster("Banned by Giovanni"):
        with Cluster("Do Not Use"):
            # hari \
            #     - Edge(color='red', style="dashed") \
            Jenkins("Jenkins") \
                << Edge(label="banned", color='red', style="dashed") \
                << giovanni
            # github_actions \
            #     << Edge(label="I will just about tolerate this") \
            #     << giovanni

    slack = Slack("Slack")

    hari \
        >> Edge(label="Hey Guys,\nlook what I just did\nthis weekend!") \
        >> slack
    ravi \
        >> Edge(label="Hey,\nwhat did I miss?") \
        >> slack
    giovanni \
        >> Edge(label="Hari is doing his\n\"rain man\"\nthing again...") \
        >> slack

    you >> readme  # << users
