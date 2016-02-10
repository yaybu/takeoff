from touchdown.core.resource import Resource


class Workspace(Resource):

    resource_name = "workspace"
    dot_ignore = True

    def __init__(self):
        super(Workspace, self).__init__(None)

    @property
    def workspace(self):
        return self

    def load(self):
        pass


class Takeofffile(Workspace):

    resource_name = "touchdown_file"

    def load(self):
        g = {"workspace": self}
        with open("Takeofffile") as f:
            code = compile(f.read(), "Takeofffile", "exec")
            exec(code, g)
