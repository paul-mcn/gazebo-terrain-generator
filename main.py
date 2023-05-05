from controllers.terrain_generator import TerrainGeneratorController
from models.terrain_generator import TerrainGeneratorModel
from views.base_view import BaseView


def main():
    # Create Model, View, and Controller
    model = TerrainGeneratorModel()
    controller = TerrainGeneratorController(model)
    view = BaseView(controller)
    controller.set_view(view)
    view.mainloop()


if __name__ == "__main__":
    main()
