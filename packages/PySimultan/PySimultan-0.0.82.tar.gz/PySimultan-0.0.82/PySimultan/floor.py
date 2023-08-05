import numpy as np
import itertools
import uuid
import weakref

# user defined imports:
from PySimultan.base_classes import GeoBaseClass
from PySimultan import settings


class Floor(GeoBaseClass):
    """
    floor class.
    """

    visible_class_name = 'Floor'
    new_floor_id = itertools.count()

    def __init__(self,
                 floor_id=None,
                 layers=None,
                 name=None,
                 is_visible=True,
                 floor_height=0,
                 storey_height=2.5,
                 color=np.append(np.random.rand(1, 3), 0)*255,
                 color_from_parent=False
                 ):
        """

        :param floor_id:
        :param layers:
        :param name:
        :param is_visible:
        :param floor_height: height from ground to the floor [m]
        :param storey_height: height from the floor to the ceiling [m]
        :param color:
        :param color_from_parent:
        """

        super().__init__(id=floor_id,
                         pid=next(self.new_floor_id),
                         color=color,
                         name=name,
                         color_from_parent=color_from_parent,
                         is_visible=is_visible,
                         layers=layers
                         )

        self._StoreyHeight = None   # StoreyHeight: height from the floor to the ceiling
        self._FloorHeight = None    # height from ground to the floor
        self._InstancesOnFloor = list()

        self.FloorHeight = floor_height
        self.StoreyHeight = storey_height

        # add to the collection
        settings.building_collection.Floor_collection.append(self)

    @property
    def FloorHeight(self):
        return self._FloorHeight

    @FloorHeight.setter
    def FloorHeight(self, value):
        """
        Position setter method
        :param value: tuple; first item is the value, second item is dict with additional parameters
        :return:
        """
        self._default_set_handling('FloorHeight', value)

    @property
    def StoreyHeight(self):
        return self._StoreyHeight

    @StoreyHeight.setter
    def StoreyHeight(self, value):
        """
        Position setter method
        :param value: tuple; first item is the value, second item is dict with additional parameters
        :return:
        """
        self._default_set_handling('StoreyHeight', value)

    @property
    def InstancesOnFloor(self, weak=True):

        if weak:
            list = list()
            for instance in self._InstancesOnFloor:
                list.append(instance())
            return list
        else:
            return self._InstancesOnFloor

    @InstancesOnFloor.setter
    def InstancesOnFloor(self, value):
        """
        Position setter method
        :param value: tuple; first item is the value, second item is dict with additional parameters
        :return:
        """
        self._default_set_handling('ObjectsOnFloor', value)

    def add_instance(self, instance):
        if not(instance in self.InstancesOnFloor):
            new_list = self._InstancesOnFloor.append(weakref.ref(instance))
            self.InstancesOnFloor = new_list
        else:
            print('instance to add already present in list')

    def remove_instance(self, instance):
        if instance in self.InstancesOnFloor:
            index_to_remove = self.InstancesOnFloor.index(instance)
            del self._InstancesOnFloor[index_to_remove]
        else:
            print('instance to remove not present in list')

