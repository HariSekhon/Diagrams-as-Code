#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: [% DATE  # 2023-04-14 13:54:52 +0100 (Fri, 14 Apr 2023) %]
#
#  https://github.com/HariSekhon/Templates
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/HariSekhon
#

"""

RabbitMQ with custom downloaded icon

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

# https://diagrams.mingrammer.com/docs/getting-started/examples

from urllib.request import urlretrieve

from diagrams import Diagram, Cluster
from diagrams.custom import Custom

from diagrams.aws.database import Aurora

from diagrams.k8s.compute import Pod

# pylint: disable=C0103
rabbitmq_url = "https://jpadilla.github.io/rabbitmqapp/assets/img/icon.png"
rabbitmq_icon = "rabbitmq.png"

urlretrieve(rabbitmq_url, rabbitmq_icon)

# pylint: disable=W0106
with Diagram("RabbitMQ Broker with custom icon", show=True):
    with Cluster("Consumers"):
        consumers = [
            Pod("worker"),
            Pod("worker"),
            Pod("worker")]

    queue = Custom("Message queue", rabbitmq_icon)

    queue >> consumers >> Aurora("Database")
