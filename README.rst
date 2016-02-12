=========
Takeoff
=========

.. image:: https://img.shields.io/travis/yaybu/takeoff/master.svg
   :target: https://travis-ci.org/#!/yaybu/takeoff

.. image:: https://img.shields.io/appveyor/ci/yaybu/takeoff/master.svg
   :target: https://ci.appveyor.com/project/yaybu/takeoff

.. image:: https://img.shields.io/codecov/c/github/yaybu/takeoff/master.svg
   :target: https://codecov.io/github/yaybu/takeoff?ref=master

.. image:: https://img.shields.io/pypi/v/takeoff.svg
   :target: https://pypi.python.org/pypi/takeoff/

.. image:: https://img.shields.io/badge/docs-latest-green.svg
   :target: http://docs.yaybu.com/projects/takeoff/en/latest/


Takeoff is a service orchestration framework for python. It provides a python
"DSL" for declaring complicated cloud infrastructures and provisioning those
blueprints in an idempotent way.

You can find us in #yaybu on irc.oftc.net.

Here is an example ``Takeofffile``::

    aws = workspace.add_aws(
        region='eu-west-1',
    )

    vpc = aws.add_virtual_private_cloud(name='example')
    vpc.add_internet_gateway(name="internet")

    example = vpc.add_subnet(
        name='application',
        cidr_block='192.168.0.0/24',
    )

    asg = aws.add_autoscaling_group(
        name='example',
        launch_configuration=aws.add_launch_configuration(
            name="example",
            ami='ami-62366',
            subnets=[example],
        ),
    )

You can then apply this configuration with::

    takeoff apply
