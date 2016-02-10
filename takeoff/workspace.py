from touchdown.core.resource import Resource
from touchdown.core import plan, workspace


class Workspace(Resource):

    resource_name = "workspace2"
    dot_ignore = True

    def __init__(self):
        super(Workspace, self).__init__(None)

    @property
    def workspace(self):
        return self

    def load(self):
        pass


class Takeofffile(Workspace):

    resource_name = "takeoff_file"

    def load(self):
        g = {"workspace": self}
        with open("Takeofffile") as f:
            code = compile(f.read(), "Takeofffile", "exec")
            exec(code, g)


class BuildWorkspace(plan.Plan):

    name = "takeoff::build-workspace"
    resource = Workspace

    def setup(self):
        self.workspace = workspace.Workspace()
