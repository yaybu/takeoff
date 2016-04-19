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

    account = workspace.add_aws_account()

    aws = account.add_environment(
        name="production",
        cidr_block="10.30.0.0/20"
    )

    nat = aws.add_nat_gateway(
        name="nat_gateway",
    )

    load_balancer = aws.add_load_balancer(
        name="load_balancer",
        public=True,
    )

    postgres = aws.add_postgres(
        name="postgres",
    )

    redis = aws.add_redis(
        name="redis",
    )

    web = aws.add_auto_scaling_group(
        name="web",
        load_balancers=[load_balancer],
        user_data={
            "DATABASE_URL": postgres.get_property("Url"),
            "REDIS_URL": redis.get_property("Url"),
        },
    )

    worker = aws.add_auto_scaling_group(
        name="worker",
        user_data={
            "DATABASE_URL": postgres.get_property("Url"),
            "REDIS_URL": redis.get_property("Url"),
        },
    )

    #web_distribution = aws.add_web_distribution(
    #    domains=['www.example.com'],
    #)

You can then apply this configuration with::

    takeoff apply
