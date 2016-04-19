from touchdown.core import argument
from touchdown.core import serializers

from ..serializers import Property
from . import zone


class Redis(zone.Zone):

    resource_name = "redis"

    prefix = argument.Integer(default=28)

    def get_property(self, name):
        return Property(name, serializers.Const(self))


class BuildWorkspace(zone.BuildWorkspace):

    resource = Redis

    def setup(self):
        super(BuildWorkspace, self).setup()

        account = self.runner.get_service(
            self.resource.environment.account,
            self.name,
        )

        self.cache = account.aws.add_replication_group(
            name=self.resource.name,
            num_cache_clusters=2,
            instance_class='cache.t2.micro',
            engine='redis',
            security_groups=[self.security_group],
            auto_minor_version_upgrade=True,
            subnet_group=account.aws.add_cache_subnet_group(
                name=self.resource.name,
                description='Subnet group for {!r}'.format(self.resource.name),
                subnets=self.subnets,
            )
        )

        self.object = {
            "Url": self.cache.get_property("Endpoint")
        }

        self.setup_cloudwatch_alarms(account)

    def setup_cloudwatch_alarms(self, account):
        self.cache.add_dependency(account.aws.add_alarm(
            name='cache-no-connections',
            namespace="AWS/ElastiCache",
            metric="CurrConnections",
            # dimensions=[{
            #      "name": "CacheClusterId",
            #      "value": "{}-shared".format(self.environment),
            # }],
            statistic='Minimum',
            period=60,
            evaluation_periods=1,
            threshold=0,
            comparison_operator='LessThanOrEqualToThreshold',
        ))
