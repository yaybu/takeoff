from touchdown.core.resource import Resource
from touchdown.core import argument

from .zone import Zone


class Redis(Zone):

    resource_name = "redis"

    @property
    def cache_url(self):
        pass

    def setup(self):
        super(Redis, self).setup()

        self.cache = aws.add_replication_group(
            name=self.name,
            num_cache_clusters=2,
            instance_class=self.get('scaling:cache', 'class', 'cache.t2.micro'),
            engine='redis',
            security_groups=[self.security_group],
            auto_minor_version_upgrade=True,
            subnet_group=aws.add_cache_subnet_group(
                name=self.name,
                description='Subnet group for {!r}'.format(self.name),
                subnets=self.subnets,
            )
        )

    def setup_cloudwatch_alarms(self):
        self.aws.add_alarm(
            name='cache-no-connections',
            namespace="AWS/ElastiCache",
            metric="CurrConnections",
            #dimensions=[{"name": "CacheClusterId", "value": "{}-shared".format(self.environment)}],
            statistic='Minimum',
            period=60,
            evaluation_periods=1,
            threshold=0,
            comparison_operator='LessThanOrEqualToThreshold',
        )
