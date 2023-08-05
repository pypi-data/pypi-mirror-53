import weakref

import numpy as np
import itertools
import uuid
from PySimultan.self_tracking_class import SelfTrackingClass

from PySimultan.layer import Layer
from PySimultan.update_handler import UpdateHandler
from PySimultan.geo_functions import print_status


# class SelfTrackingClass(object):
#     """Use as base class for classes that can report their instances.
#
#     Subclass.instances: get list of object instances.
#     Subclass.max: get/set max number of instances; default is unlimited.
#     """
#
#     # set in Subclass to limit number of instances of Subclass
#     max = None
#
#     # key: class name as string, value: list of weakrefs to instances
#     _classnames = {}
#
#     # technique for "class properties" is adapted from:
#     #   http://stackoverflow.com/a/7864317/3531387
#     class ClassProperty(property):
#         def __get__(self, cls, owner):
#             return self.fget.__get__(None, owner)()
#
#     @ClassProperty
#     @classmethod
#     def instances(cls):
#         """Return tuple of instances for this class, or None if none."""
#         try:
#             return tuple(
#               [instance() for instance in cls._classnames[cls.__name__]])
#         except KeyError:
#             return None
#
#     def __new__(cls, **kwargs):
#         """Create instance, if not over limit, and store ref to it."""
#         if cls.__name__ not in cls._classnames:
#             cls._classnames[cls.__name__] = []
#         instance = object.__new__(cls)
#         cls._classnames[cls.__name__].append(weakref.ref(instance))
#         return instance
#
#     def __del__(self):
#         """Remove ref to dead instance from list of instances."""
#         for instance in self.__class__._classnames[self.__class__.__name__]:
#             if instance() is None:
#                 self.__class__._classnames[
#                   self.__class__.__name__].remove(instance)
#         if len(self.__class__._classnames[self.__class__.__name__]) == 0:
#             del self.__class__._classnames[self.__class__.__name__]


# class GeoBaseClass(SelfTrackingClass):
#     """Use as base class for geometry related classes
#      Classes can report their instances and track changes
#
#         Subclass.instances: get list of object instances.
#         Subclass.max: get/set max number of instances; default is unlimited.
#
#         https://codereview.stackexchange.com/questions/54627/base-class-for-subclasses-that-can-track-their-own-instances
#     """
#
#     new_id = itertools.count(0)
#
#     def __init__(self,
#                  id=None,
#                  pid=None,
#                  color=None,
#                  name=None,
#                  color_from_parent=True,
#                  is_visible=True,
#                  layers=None
#                  ):
#
#         self._observers = []
#
#         self._ID = None
#         self._PID = None
#         self._Name = None
#         self._Color = None
#         self._IsVisible = None
#         self._ColorFromParent = None
#
#         if layers is None:
#             if not Layer.get_instances:
#                 self._Layers = [Layer()]
#             else:
#                 self._Layers = [Layer.get_instances()[0]]
#         elif type(layers) == list:
#             self._Layers = layers
#         else:
#             self._Layers = [layers]
#
#         if pid is None:
#             self._PID = next(self.new_id)
#         else:
#             self._PID = pid
#
#         if name is None:
#             self._Name = 'Base{}'.format(self._PID)
#         else:
#             self._Name = name
#
#         if id is None:
#             self.ID = uuid.uuid4()
#         else:
#             self.ID = id
#         self.IsVisible = is_visible
#         self.Color = color
#         self.ColorFromParent = color_from_parent
#
#         self._UpdateHandler = UpdateHandler()
#
#         # -----------------------------------------------
#         # bindings
#
#         for layer in self._Layers:
#             layer.bind_to(self.layer_updated)
#
#     @property
#     def ID(self):
#         return self._ID
#
#     @ID.setter
#     def ID(self, value):
#         self._default_set_handling('ID', value)
#
#     @property
#     def PID(self):
#         return self._PID
#
#     @PID.setter
#     def PID(self, value):
#         self._default_set_handling('PID', value)
#
#     @property
#     def Layers(self):
#         return self._Layers
#
#     @Layers.setter
#     def Layers(self, value):
#         self._default_set_handling('Layers', value)
#
#     @property
#     def Name(self):
#         return self._Name
#
#     @Name.setter
#     def Name(self, value):
#         self._default_set_handling('Name', value)
#
#     @property
#     def Color(self):
#         if self._Color is None:
#             self.Color = create_random_color()
#         return self._Color
#
#     @Color.setter
#     def Color(self, value):
#         self._default_set_handling('Color', value)
#
#     @property
#     def IsVisible(self):
#         return self._IsVisible
#
#     @IsVisible.setter
#     def IsVisible(self, value):
#         self._default_set_handling('IsVisible', value)
#
#     @property
#     def ColorFromParent(self):
#         return self._ColorFromParent
#
#     @ColorFromParent.setter
#     def ColorFromParent(self, value):
#         self._default_set_handling('ColorFromParent', value)
#
#     def bind_to(self, callback):
#         if callback not in self._observers:
#             self._observers.append(callback)
#
#     def unbind(self, callback):
#         if callback in self._observers:
#             self._observers.remove(callback)
#
#     def _default_set_handling(self, attr_name, value, bind_method=None):
#
#         default_notification = True
#
#         # check bindings
#         if hasattr(self, '_' + attr_name):
#
#             old_values = getattr(self, '_' + attr_name)
#
#             if np.array(old_values == value).all():
#                 return
#
#             old_values = getattr(self, '_' + attr_name)
#             if old_values is not None:
#                 if not isinstance(old_values, list):
#                     old_values = [old_values]
#
#                 for old_value in old_values:
#                     if hasattr(old_value, 'bind_to'):
#                         for observer in old_value._observers:
#                             if observer.__self__ == old_value:
#                                 old_value.remove(observer)
#
#         if isinstance(value, tuple):
#             setattr(self, '_' + attr_name, value[0])
#             notify_observers = default_notification
#             if value.__len__() > 1:
#                 if 'notify_observers' in value[1]:
#                     notify_observers = value[1]['notify_observers']
#                 else:
#                     notify_observers = default_notification
#         else:
#             setattr(self, '_' + attr_name, value)
#             notify_observers = default_notification
#
#         if notify_observers:
#
#             for callback in self._observers:
#                 instance = callback.__self__
#                 instance._UpdateHandler.add_notification(callback, attr_name)
#                 # callback(ChangedAttribute=attr_name)
#
#         if bind_method is not None:
#             for instance in getattr(self, '_' + attr_name):
#                 instance.bind_to(bind_method)
#
#     def start_bulk_update(self):
#         self._UpdateHandler.BulkUpdate = True
#
#     def end_bulk_update(self):
#         self._UpdateHandler.BulkUpdate = False
#
#     # --------------------------------------------------------
#     # observed object change callbacks
#     # --------------------------------------------------------
#
#     def layer_updated(self, **kwargs):
#         for key, value in kwargs.items():
#             if value == 'vertex_position_changed':
#                 for callback in self._observers:
#                     callback(ChangedAttribute='vertex_position_changed')
#
#     def print_status(self, *args, **kwargs):
#         print(*args, **kwargs)


class ObjectBaseClass(SelfTrackingClass):

    new_id = itertools.count(0)

    def __init__(self,
                 id=None,
                 pid=None,
                 color=None,
                 name=None,
                 color_from_parent=True,
                 is_visible=True,
                 ):

        self._observers = []
        self._observed = []

        self._ID = None
        self._PID = None
        self._Name = None
        self._Color = None
        self._IsVisible = None
        self._ColorFromParent = None

        if pid is None:
            self.PID = next(self.new_id)
        else:
            self.PID = pid

        if name is None:
            self.Name = 'Base{}'.format(self.PID)
        else:
            self.Name = name

        if id is None:
            self.ID = uuid.uuid4()
        else:
            self.ID = id

        self.PID = next(self.new_id)
        self.IsVisible = is_visible
        self.Color = color
        self.ColorFromParent = color_from_parent
        self._UpdateHandler = UpdateHandler()

        # -----------------------------------------------
        # bindings

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._default_set_handling('ID', value)

    @property
    def PID(self):
        return self._PID

    @PID.setter
    def PID(self, value):
        self._default_set_handling('PID', value)

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, value):
        self._default_set_handling('Name', value)

    @property
    def Color(self):
        if self._Color is None:
            self.Color = create_random_color()
        return self._Color

    @Color.setter
    def Color(self, value):
        self._default_set_handling('Color', value)

    @property
    def IsVisible(self):
        return self._IsVisible

    @IsVisible.setter
    def IsVisible(self, value):
        self._default_set_handling('IsVisible', value)

    @property
    def ColorFromParent(self):
        return self._ColorFromParent

    @ColorFromParent.setter
    def ColorFromParent(self, value):
        self._default_set_handling('ColorFromParent', value)

    def bind_to(self, callback):
        if callback not in self._observers:
            self._observers.append(callback)

    def unbind(self, callback):
        if callback in self._observers:
            self._observers.remove(callback)

    def _default_set_handling(self, attr_name, value, bind_method=None):

        default_notification = True

        # check bindings: remove all bindigs of the values to self
        if hasattr(self, '_' + attr_name):

            old_values = getattr(self, '_' + attr_name)

            if np.array(old_values == value).all():
                return

            if old_values is not None:
                if not isinstance(old_values, list):
                    old_values = [old_values]
                # print('old values has {n} entries'.format(n=old_values.__len__()))
                for old_value in old_values:
                    if hasattr(old_value, '_observers'):
                        # print('{instance} has {n} observers.'.format(instance=old_value, n=old_value._observers.__len__()))
                        for observer_method in old_value._observers:
                            # print(observer_method.__self__)
                            if observer_method.__self__ == self:
                                old_value._observers.remove(observer_method)
                                # print('removing observer method {method} from {instance} observers'.format(method=observer_method, instance=old_value))

        if isinstance(value, tuple):
            setattr(self, '_' + attr_name, value[0])
            notify_observers = default_notification
            if value.__len__() > 1:
                if 'notify_observers' in value[1]:
                    notify_observers = value[1]['notify_observers']
                else:
                    notify_observers = default_notification
        else:
            setattr(self, '_' + attr_name, value)
            notify_observers = default_notification

        if notify_observers:

            for callback in self._observers:
                instance = callback.__self__
                instance._UpdateHandler.add_notification(callback, attr_name)

        if bind_method is not None:
            instances = getattr(self, '_' + attr_name)

            if instances is None:
                return
            elif not isinstance(instances, list):
                instances = [instances]

            for instance in instances:
                if hasattr(instance, 'bind_to'):
                    # print('bind {instance} to {method})'.format(instance=instance, method=bind_method))
                    if not(bind_method in instance._observers):
                        instance.bind_to(bind_method)
                        self._observed.append(instance)

    def start_bulk_update(self):
        self._UpdateHandler.BulkUpdate = True

    def end_bulk_update(self):
        self._UpdateHandler.BulkUpdate = False

    def print_status(self, *args, **kwargs):
        print_status(*args, **kwargs)

    # --------------------------------------------------------
    # observed object change callbacks
    # --------------------------------------------------------


class TrackedClass(SelfTrackingClass):

    def __init__(self):

        self._observers = []
        self._UpdateHandler = UpdateHandler()

    def bind_to(self, callback):
        if callback not in self._observers:
            self._observers.append(callback)

    def unbind(self, callback):
        if callback in self._observers:
            self._observers.remove(callback)

    def _default_set_handling(self, attr_name, value):
        default_notification = True

        if isinstance(value, tuple):
            setattr(self, '_' + attr_name, value[0])
            notify_observers = default_notification
            if value.__len__() > 1:
                if 'notify_observers' in value[1]:
                    notify_observers = value[1]['notify_observers']
                else:
                    notify_observers = default_notification
        else:
            setattr(self, '_' + attr_name, value)
            notify_observers = default_notification

        if notify_observers:

            for callback in self._observers:
                instance = callback.__self__
                instance._UpdateHandler.add_notification(callback, attr_name)
                # callback(ChangedAttribute=attr_name)

    def print_status(self, *args, **kwargs):
        print_status(*args, **kwargs)


class GeoBaseClass(ObjectBaseClass):

    new_id = itertools.count(0)

    def __init__(self,
                 id=None,
                 pid=None,
                 color=None,
                 name=None,
                 color_from_parent=True,
                 is_visible=True,
                 layers=None
                 ):

        super().__init__(id=id,
                         pid=pid,
                         color=color,
                         name=name,
                         color_from_parent=color_from_parent,
                         is_visible=is_visible)

        self._Layers = None

        if layers is None:
            if not Layer.get_instances:
                self._Layers = [Layer()]
            else:
                self._Layers = [Layer.get_instances()[0]]
        elif type(layers) == list:
            self._Layers = layers
        else:
            self._Layers = [layers]

        # -----------------------------------------------
        # bindings

        # for layer in self._Layers:
        #     layer.bind_to(self.layer_updated)

    @property
    def Layers(self):
        return self._Layers

    @Layers.setter
    def Layers(self, value):
        self._default_set_handling('Layers', value, bind_method=self.layer_updated)

    def layer_updated(self, **kwargs):
        for key, value in kwargs.items():
            if value == 'vertex_position_changed':
                for callback in self._observers:
                    callback(ChangedAttribute='vertex_position_changed')


def create_random_color():
    return np.append(np.random.rand(1, 3), 0)*255




