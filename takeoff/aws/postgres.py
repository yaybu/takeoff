from touchdown.core.resource import Resource

from . import zone


class Postgres(zone.Zone):

    resource_name = "postgres"

    @property
    def database_url(self):
        pass


class BuildWorkspace(zone.BuildWorkspace):

    resource = Postgres

    def setup(self):
        super(BuildWorkspace, self).setup()

        env = self.runner.get_service(self.resource.environment, self.name)
        account = self.runner.get_service(self.resource.environment.account, self.name)

        self.database = account.aws.add_database(
            name=self.resource.name,
            allocated_storage='10',
            instance_class='db.t1.micro',
            engine="postgres",
            engine_version="9.3.6",
            db_name=self.name,
            master_username="root",
            master_password="password",
            backup_retention_period=8,
            multi_az=True,
            auto_minor_version_upgrade=True,
            iops=None,
            publically_accessible=self.resource.public,
            storage_encrypted='no',
            storage_type="gp2",
            security_groups=[self.security_group],
            subnet_group=account.aws.add_db_subnet_group(
                name=self.resource.name,
                description="Subnet group for {!r}".format(self.resource.name),
                subnets=self.subnets,
            )
        )

    def setup_cloudwatch_alarms(self):
        self.aws.add_alarm(
            name='database-no-connections',
            namespace="AWS/RDS",
            metric="DatabaseConnections",
            dimensions=[{"name": "DBInstanceIdentifier", "value": self.name}],
            statistic='Minimum',
            period=60,
            evaluation_periods=1,
            threshold=0,
            comparison_operator='LessThanOrEqualToThreshold',
        )
