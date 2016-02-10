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
        self.database = aws.add_database(
            name=self.name,
            allocated_storage=self.get('scaling:database', 'storage', '10'),
            instance_class=self.get('scaling:database', 'class', 'db.t1.micro'),
            engine="postgres",
            engine_version="9.3.6",
            db_name=self.name,
            master_username="root",
            master_password=self.get("postgres", "password"),
            backup_retention_period=8,
            multi_az=True,
            auto_minor_version_upgrade=True,
            iops=self.get('scaling:database', 'iops', None) or None,
            publically_accessible=self.public,
            storage_encrypted=self.get('scaling:database', 'encrypted', 'yes') == 'yes',
            storage_type="gp2",
            security_groups=[self.security_group],
            subnet_group=aws.add_db_subnet_group(
                name=self.name,
                description="Subnet group for {!r}".format(self.name),
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
