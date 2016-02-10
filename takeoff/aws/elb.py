from touchdown.core.resource import Resource
from touchdown.core import argument

from .zone import Zone


class LoadBalancer(Zone):

    resource_name = "load_balancer"

    def setup(self):
        self.load_balancer = aws.add_load_balancer(
            name='balancer',
            listeners=[{"port": 443, "instance_port": 8043, "instance_protocol": "TCP", "protocol": "TCP"}],
            subnets=self.subnets,
            security_groups=[self.security_group],
            health_check={
                "interval": 30,
                "healthy_threshold": 3,
                "unhealthy_threshold": 5,
                "check": "HTTPS:8043/__ping__",
                "timeout": 20,
            },
            cross_zone_load_balancing=True,
            connection_draining=30,
        )

        # FIXME: Add DNS record for load balancer???


    def setup_cloudwatch_alarm(self):
        self.aws.add_alarm(
            name='balancer-not-enough-healthy-instances',
            namespace="AWS/ELB",
            metric="HealthyHostCount",
            dimensions=[{"name": "LoadBalancerName", "value": "balancer"}],
            statistic='Minimum',
            period=60,
            evaluation_periods=1,
            threshold=self.scaling_groups['application']['min'],
            comparison_operator='LessThanThreshold',
        )

        # FIXME: Base period and evaluation on the ELB settings - this should help
        # avoid false positives?
        self.aws.add_alarm(
            name='balancer-unhealthy-instances',
            namespace="AWS/ELB",
            metric="UnHealthyHostCount",
            dimensions=[{"name": "LoadBalancerName", "value": "balancer"}],
            statistic='Average',
            period=60,
            evaluation_periods=1,
            threshold=1,
            comparison_operator='GreaterThanOrEqualToThreshold',
        )

        self.aws.add_alarm(
            name='balancer-high-latency',
            dimensions=[{"name": "LoadBalancerName", "value": "balancer"}],
            namespace="AWS/ELB",
            metric="Latency",
            statistic='Average',
            period=60,
            evaluation_periods=1,
            threshold=1,
            comparison_operator='GreaterThanOrEqualToThreshold',
        )

        self.aws.add_alarm(
            name='balancer-queue-length',
            namespace="AWS/ELB",
            metric="SurgeQueueLength",
            dimensions=[{"name": "LoadBalancerName", "value": "balancer"}],
            statistic='Maximum',
            period=60,
            evaluation_periods=1,
            threshold=0,
            comparison_operator='GreaterThanThreshold',
        )

        self.aws.add_alarm(
            name='balancer-queue-spillover',
            namespace="AWS/ELB",
            metric="SpilloverCount",
            dimensions=[{"name": "LoadBalancerName", "value": "balancer"}],
            statistic='Sum',
            period=60,
            evaluation_periods=1,
            threshold=0,
            comparison_operator='GreaterThanThreshold',
        )
