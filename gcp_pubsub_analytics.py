#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-14 13:54:52 +0100 (Fri, 14 Apr 2023)
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

GCP PubSub Analytics

"""

# based on https://diagrams.mingrammer.com/docs/getting-started/examples
__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from diagrams import Diagram, Cluster

# GCP resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/gcp
#
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import BigTable
from diagrams.gcp.iot import IotCore
from diagrams.gcp.storage import GCS

# pylint: disable=W0106
with Diagram("GCP PubSub Analytics", show=not bool(os.environ.get('CI', 0))):
    pubsub = PubSub("GCP Pub/Sub")

    with Cluster("Data Sources"):
        [IotCore("IoT Core1"),
         IotCore("IoT Core2"),
         IotCore("IoT Core3")] >> pubsub

    with Cluster("Analytics Destinations"):
        with Cluster("Streaming"):
            dataflow = Dataflow("Data Flow")

        with Cluster("Data Lake"):
            dataflow >> [BigQuery("BigQuery"), GCS("GCS\nBlob Storage")]

        with Cluster("Event Driven"):
            with Cluster("Processing"):
                dataflow >> AppEngine("AppEngine") >> BigTable("BigTable")

            with Cluster("Serverless"):
                dataflow >> Functions("Cloud Functions") >> AppEngine("AppEngine")

    # pylint: disable=W0104
    pubsub >> dataflow
