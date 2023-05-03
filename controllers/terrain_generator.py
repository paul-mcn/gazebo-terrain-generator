class TerrainGeneratorController:
    """docstring for Controller."""

    def __init__(self, model):
        super(TerrainGeneratorController, self).__init__()
        self.model = model
        self.view = None

    def set_x(self, value):
        self.model.x = float(value)
        if self.view:
            self.view.viewport.draw_scene()

    def set_y(self, value):
        self.model.y = float(value)
        if self.view:
            self.view.viewport.draw_scene()

    def set_z(self, value):
        self.model.z = float(value)
        if self.view:
            self.view.viewport.draw_scene()

    def set_max_angle(self, value):
        self.model.set_max_angle(value)

    def set_foliage_density(self, value):
        self.model.set_foliage_density(value)

    def get_x(self):
        return self.model.x

    def get_y(self):
        return self.model.y

    def get_z(self):
        return self.model.z

    def set_view(self, view):
        self.view = view

    def get_max_angle(self):
        return self.model.max_angle

    def get_foliage_density(self):
        return self.model.foliage_density
