class ControladorCamara:
    def __init__(self, id, description, is_default):
        self._id = id
        self._description = description
        self._is_default = is_default

    def id(self):
        return self._id

    def description(self):
        return self._description

    def isDefault(self):
        return self._is_default