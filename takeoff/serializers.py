from touchdown.core import errors, serializers


class Property(serializers.Serializer):

    def __init__(self, property, inner=serializers.Identity()):
        self.property = property
        self.inner = inner

    def render(self, runner, object):
        target = self.inner.render(runner, object)
        target_plan = runner.get_service(target, "takeoff::build-workspace")
        if self.property not in target_plan.object:
            raise errors.Error("{} not available".format(self.property))
        return target_plan.object[self.property]

    def dependencies(self, object):
        return self.inner.dependencies(object)
