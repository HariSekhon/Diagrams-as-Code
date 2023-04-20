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

RabbitMQ Broker with custom icon

"""

# based on https://diagrams.mingrammer.com/docs/getting-started/examples

__author__ = 'Hari Sekhon'
__version__ = '0.2'

import os
from urllib.request import urlretrieve

from diagrams import Diagram, Cluster

from diagrams.custom import Custom
from diagrams.aws.database import Aurora
from diagrams.k8s.compute import Pod

# pylint: disable=C0103
rabbitmq_url = "https://jpadilla.github.io/rabbitmqapp/assets/img/icon.png"
rabbitmq_icon = "rabbitmq.png"

# XXX: filename=images/ changes the $PWD so rabbitmq_icon path must be local dir,
# but at this point we're still at top level dir
urlretrieve(rabbitmq_url, os.path.join("images", rabbitmq_icon) )

# pylint: disable=W0106
with Diagram("RabbitMQ Broker with custom icon",
             show=not bool(os.environ.get('CI', 0)),
             filename='images/rabbitmq_broker_with_custom_icon',
             ):
    with Cluster("Consumers"):
        consumers = [
            Pod("worker"),
            Pod("worker"),
            Pod("worker")]

    rabbitmq = Custom("RabbitMQ", rabbitmq_icon)

    rabbitmq >> consumers >> Aurora("Database")

#os.remove(rabbitmq_icon)
