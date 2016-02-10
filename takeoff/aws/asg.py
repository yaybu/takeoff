from touchdown.core.resource import Resource
from touchdown.core import argument

from .elb import LoadBalancer
from . import zone


class AutoScalingGroup(zone.Zone):

    resource_name = "auto_scaling_group"

    replacement_policy = argument.String(
        choices=['singleton', 'graceful'],
    )

    load_balancers = argument.ResourceList(
        LoadBalancer,
    )

    user_data = argument.Dict()


class BuildWorkspace(zone.BuildWorkspace):

    resource = AutoScalingGroup

    def setup(self):
        lc_kwargs = {}
        if 'role' in group:
            lc_kwargs['instance_profile'] = instance_profiles[group['role']]

        self.auto_scaling_group = aws.add_auto_scaling_group(
            name=name,
            launch_configuration=aws.add_launch_configuration(
                name=name,
                image=group['ami'],
                instance_type=group['class'],
                user_data=self.user_data(name, group),
                key_pair=self.environment.keypair,
                security_groups=[self.security_group],
                associate_public_ip_address=self.public,
                **lc_kwargs
            ),
            min_size=group["min"],
            max_size=group["max"],
            replacement_policy=self.replacement_policy,
            load_balancers=[lb.load_balancer for lb in self.load_balancers],
            subnets=self.subnets,
        )
