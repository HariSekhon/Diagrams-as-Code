#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-18 17:42:57 +0100 (Tue, 18 Apr 2023)
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

# ported from here:
#
#   https://cloudgram.dedalusone.com/examples.html

"""

AWS Serverless Image Processing

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from diagrams import Diagram, Cluster

# ============================================================================ #
# AWS resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/aws
#

from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import Appsync, StepFunctions
from diagrams.aws.ml import Rekognition
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3
from diagrams.aws.general import User

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "splines": "spline",  # rounded arrows, much nicer
}

# diagram name results in 'web_service.png' as the output name
# pylint: disable=W0104,W0106
with Diagram('AWS Serverless Image Processing',
             show=not bool(os.environ.get('CI', 0)),
             filename='images/aws_serverless_image_processing',
             graph_attr=graph_attr,
             ):
    appsync = Appsync("AWS AppSync")

    user = User("User")

    user >> Cognito("AWS Cognito")

    user \
        >> S3("AWS S3 Bucket") \
        >> Lambda("Start workflow") \
        >> appsync

    user >> appsync

    resolver = Lambda("AWS Resolver")

    with Cluster("Backend"):
        dynamodb = Dynamodb("AWS DynamoDB")
        appsync \
            >> resolver \
            >> dynamodb

        step_function = StepFunctions("AWS Step Function")
        resolver \
            >> step_function

        step_function \
            >> Lambda("Create thumbnail")

        step_function \
            >> Lambda("Persist Metadata") \
            >> dynamodb

        step_function \
            >> Lambda("Extract metadata")

        step_function \
            >> Lambda("Object / Scene detection") \
            >> Rekognition("AWS Rekognition")
