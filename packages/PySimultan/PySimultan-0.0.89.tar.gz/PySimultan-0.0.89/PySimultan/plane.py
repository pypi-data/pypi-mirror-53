from PySimultan.base_classes import GeoBaseClass
import itertools
import numpy as np

from PySimultan import settings


class Plane(GeoBaseClass):

    new_plane_id = itertools.count(0)
    visible_class_name = 'Plane'

    def __init__(self,
                 origin=None,
                 normal=None,
                 plane_id=None,
                 color=None,
                 name=None,
                 color_from_parent=True,
                 is_visible=True,
                 layers=None):

        super().__init__(id=plane_id,
                         pid=next(type(self).new_plane_id),
                         color=color,
                         name=name,
                         color_from_parent=color_from_parent,
                         is_visible=is_visible,
                         layers=layers
                         )

        self._Origin = None
        self._Normal = None

        if origin is not None:
            self.Origin = origin
        else:
            self.Origin = np.array([0, 0, 0])

        if normal is not None:
            self.Normal = normal
        else:
            self.Normal = np.array([0, 0, 1])

        settings.building_collection.Plane_collection.append(self)

    @property
    def Origin(self):
        return self._Origin

    @Origin.setter
    def Origin(self, value):
        self._default_set_handling('Origin', value)

    @property
    def Normal(self):
        return self._Normal

    @Normal.setter
    def Normal(self, value):
        self._default_set_handling('Normal', value)