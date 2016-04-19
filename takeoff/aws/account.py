import json

from touchdown.core.resource import Resource
from touchdown.core import argument, plan

from takeoff.workspace import Takeofffile


class Account(Resource):

    resource_name = "aws_account"

    root = argument.Resource(Takeofffile)


class BuildWorkspace(plan.Plan):

    name = "takeoff::build-workspace"
    resource = Account

    def setup(self):
        ws = self.runner.get_service(self.resource.workspace, self.name)
        self.aws = ws.workspace.add_aws(
            region="eu-west-1",
            access_key_id="",
            secret_access_key="",
            mfa_serial="",
        )

        if True:
            self.aws = self.aws.add_external_role(
                name='',
                arn='',
            )

        self.setup_cloudtrail_logs()
        self.setup_cloudtrail()
        self.setup_cloudtrail_metrics()
        self.setup_cloudtrail_alarms()

    def get_cloudtrail_arn(self):
        return (
            "arn:aws:logs:*:*:log-group:cloudtrail.log:log-stream:*CloudTrail*"
        )

    def setup_cloudtrail(self):
        bucket_name = "cloudtrail"

        bucket = self.aws.add_bucket(
            name=bucket_name,
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AWSCloudTrailAclCheck20131101",
                        "Effect": "Allow",
                        "Principal": {"AWS": [
                            "arn:aws:iam::903692715234:root",
                            "arn:aws:iam::035351147821:root",
                            "arn:aws:iam::859597730677:root",
                            "arn:aws:iam::814480443879:root",
                            "arn:aws:iam::216624486486:root",
                            "arn:aws:iam::086441151436:root",
                            "arn:aws:iam::388731089494:root",
                            "arn:aws:iam::284668455005:root",
                            "arn:aws:iam::113285607260:root"
                        ]},
                        "Action": "s3:GetBucketAcl",
                        "Resource": "arn:aws:s3:::{}".format(bucket_name)
                    }, {
                        "Sid": "AWSCloudTrailWrite20131101",
                        "Effect": "Allow",
                        "Principal": {"AWS": [
                            "arn:aws:iam::903692715234:root",
                            "arn:aws:iam::035351147821:root",
                            "arn:aws:iam::859597730677:root",
                            "arn:aws:iam::814480443879:root",
                            "arn:aws:iam::216624486486:root",
                            "arn:aws:iam::086441151436:root",
                            "arn:aws:iam::388731089494:root",
                            "arn:aws:iam::284668455005:root",
                            "arn:aws:iam::113285607260:root"
                        ]},
                        "Action": "s3:PutObject",
                        "Resource": "arn:aws:s3:::{name}/AWSLogs/*".format(
                            name=bucket_name
                        ),
                        "Condition": {
                            "StringEquals": {
                                "s3:x-amz-acl": "bucket-owner-full-control"
                            }
                        }
                    }
                ],
            })
        )

        role = self.aws.add_role(
            name="cloudtrail-cwlogs",
            assume_role_policy={
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }],
            },
            policies={
                "push-logs": {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": [
                            "logs:PutLogEvents",
                            "logs:CreateLogStream",
                        ],
                        "Resource": [
                            self.get_cloudtrail_arn(),
                        ]
                    }],
                },
            },
        )

        # we call it this to match the one the AWS console creates
        self.aws.add_trail(
            name="Default",
            bucket=bucket,
            include_global=True,
            cwlogs_group=self.cloudtrail_log,
            cwlogs_role=role,
        )

    def setup_cloudtrail_logs(self):
        self.cloudtrail_log = self.aws.add_log_group(
            name="cloudtrail.log",
            retention=7,
        )

    def setup_cloudtrail_metrics(self):
        self.cloudtrail_log.add_filter(
            name='security_group_changes',
            pattern=(
                '{ ($.eventName = AuthorizeSecurityGroupIngress) || '
                '($.eventName = AuthorizeSecurityGroupEgress) || '
                '($.eventName = RevokeSecurityGroupIngress) || '
                '($.eventName = RevokeSecurityGroupEgress) || '
                '($.eventName = CreateSecurityGroup) || '
                '($.eventName = DeleteSecurityGroup) }'
            ),
            transformations=[{
                "name": "SecurityGroupChange",
                "namespace": "CloudTrail",
                "value": 1,
            }]
        )

        self.cloudtrail_log.add_filter(
            name='network_acl_changes',
            pattern=(
                '{ ($.eventName = CreateNetworkAcl) || '
                '($.eventName = CreateNetworkAclEntry) || '
                '($.eventName = DeleteNetworkAcl) || '
                '($.eventName = DeleteNetworkAclEntry) || '
                '($.eventName = ReplaceNetworkAclEntry) || '
                '($.eventName = ReplaceNetworkAclAssociation) }'
            ),
            transformations=[{
                "name": "NetworkACLChange",
                "namespace": "CloudTrail",
                "value": 1,
            }]
        )

        self.cloudtrail_log.add_filter(
            name='internet_gateway_changes',
            pattern=(
                '{ ($.eventName = CreateCustomerGateway) || '
                '($.eventName = DeleteCustomerGateway) || '
                '($.eventName = AttachInternetGateway) || '
                '($.eventName = CreateInternetGateway) || '
                '($.eventName = DeleteInternetGateway) || '
                '($.eventName = DetachInternetGateway) }'
            ),
            transformations=[{
                "name": "InternetGatewayChange",
                "namespace": "CloudTrail",
                "value": 1,
            }]
        )

        self.cloudtrail_log.add_filter(
            name='cloudtrail_changes',
            pattern=(
                '{ ($.eventName = CreateTrail) || '
                '($.eventName = UpdateTrail) || '
                '($.eventName = DeleteTrail) || '
                '($.eventName = StartLogging) || '
                '($.eventName = StopLogging) }'
            ),
            transformations=[{
                "name": "CloudTrailChange",
                "namespace": "CloudTrail",
                "value": 1,
            }]
        )

        self.cloudtrail_log.add_filter(
            name='signin_failures',
            pattern=(
                '{ ($.eventName = ConsoleLogin) && '
                '($.errorMessage = "Failed authentication") }'
            ),
            transformations=[{
                "name": "SigninFailure",
                "namespace": "CloudTrail",
                "value": 1,
            }]
        )

        self.cloudtrail_log.add_filter(
            name='authorization_failures',
            pattern=(
                '{ ($.errorCode = "*UnauthorizedOperation") || '
                '($.errorCode = "AccessDenied*") }'
            ),
            transformations=[{
                "name": "AuthorizationFailure",
                "namespace": "CloudTrail",
                "value": 1,
            }]
        )

        self.cloudtrail_log.add_filter(
            name='iam_policy_changes',
            pattern=(
                '{($.eventName=DeleteGroupPolicy)||'
                '($.eventName=DeleteRolePolicy)||'
                '($.eventName=DeleteUserPolicy)||'
                '($.eventName=PutGroupPolicy)||'
                '($.eventName=PutRolePolicy)||'
                '($.eventName=PutUserPolicy)||'
                '($.eventName=CreatePolicy)||'
                '($.eventName=DeletePolicy)||'
                '($.eventName=CreatePolicyVersion)||'
                '($.eventName=DeletePolicyVersion)||'
                '($.eventName=AttachRolePolicy)||'
                '($.eventName=DetachRolePolicy)||'
                '($.eventName=AttachUserPolicy)||'
                '($.eventName=DetachUserPolicy)||'
                '($.eventName=AttachGroupPolicy)||'
                '($.eventName=DetachGroupPolicy)}'
            ),
            transformations=[{
                "name": "IamPolicyChange",
                "namespace": "CloudTrail",
                "value": 1,
            }]
        )

    def setup_cloudtrail_alarms(self):
        alarms = [
            ('security-group-changes', 'SecurityGroupChanges'),
            ('network-acl-changes', 'NetworkACLChange'),
            ('internet-gateway-changes', 'InternetGatewayChange'),
            ('cloudtrail-changes', 'CloudTrailChange'),
            ('signin-failures', 'SigninFailure'),
            ('authorization-failures', 'AuthorizationFailure'),
            ('iam-policy-changes', 'IamPolicyChange'),
        ]

        for alarm_name, metric_name in alarms:
            alarm = self.aws.add_alarm(
                name=alarm_name,
                namespace="CloudTrail",
                metric=metric_name,
                statistic='Sum',
                period=5 * 60,
                evaluation_periods=1,
                threshold=1,
                comparison_operator='GreaterThanOrEqualToThreshold',
            )
            alarm.add_dependency(self.cloudtrail_log)
