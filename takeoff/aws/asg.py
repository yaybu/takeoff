from touchdown.core import argument, serializers

from .elb import LoadBalancer
from . import zone


class AutoScalingGroup(zone.Zone):

    resource_name = "auto_scaling_group"

    name = argument.String()

    replacement_policy = argument.String(
        choices=['singleton', 'graceful'],
    )

    load_balancers = argument.ResourceList(
        LoadBalancer,
    )

    user_data = argument.Dict()

    def clean_user_data(self, value):
        value = serializers.Dict(**value)
        for dep in value.dependencies(self):
            if dep != self:
                self.add_dependency(dep)
        return value


class BuildWorkspace(zone.BuildWorkspace):

    resource = AutoScalingGroup

    def setup(self):
        super(BuildWorkspace, self).setup()

        env = self.runner.get_service(self.resource.environment, self.name)
        account = self.runner.get_service(self.resource.environment.account, self.name)

        user_data = serializers.Json(serializers.Dict(**self.resource.user_data.render(
            self.runner,
            self.resource.user_data
        )))

        self.auto_scaling_group = account.aws.add_auto_scaling_group(
            name=self.resource.name,
            launch_configuration=account.aws.add_launch_configuration(
                name=self.resource.name,
                image='ami-123456',
                instance_type="t2.micro",
                user_data=user_data,
                key_pair=env.keypair,
                security_groups=[self.security_group],
                associate_public_ip_address=self.resource.public,
                # instance_profile=...
            ),
            min_size=1,
            max_size=1,
            replacement_policy=self.resource.replacement_policy,
            load_balancers=[
                self.runner.get_service(lb, self.name).load_balancer for lb in self.resource.load_balancers
            ],
            subnets=self.subnets,
        )
