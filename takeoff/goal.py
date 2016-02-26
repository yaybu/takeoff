from touchdown.core import goals, dependencies


class BuildWorkspace(goals.Goal):

    def get_plan_class(self, resource):
       return resource.meta.get_plan("null")

    def execute(self):
        depmap = list(dependencies.DependencyMap(self.workspace).all())
        workspace = self.get_service(self.workspace, "takeoff::build-workspace")
        workspace.setup()
        for resource in depmap[:-1]:
            self.get_service(resource, "takeoff::build-workspace").setup()
        return workspace.workspace
