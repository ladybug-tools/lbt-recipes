# coding: utf-8
"""Class to handle settings for running recipes locally."""
from __future__ import division
import argparse
import shlex
import os

from honeybee.typing import int_in_range


class RecipeSettings(object):
    """Parameters specifying how to run recipes locally.

    Args:
        folder: Path to a project folder in which the recipe will be executed.
            If None, the default project folder for the Recipe will be
            used. (Default: None).
        workers: An integer to set the number of CPUs used in the execution of the
            recipe. This number should not exceed the number of CPUs on the
            machine running the simulation and should be lower if other tasks
            are running while the simulation is running. If set to None, it
            should automatically default to one less than the number of CPUs
            currently available on the machine. (Default: None).
        reload_old: A boolean to indicate whether existing results for a given project
            and simulation ID should be reloaded if they are found instead of
            re-running the entire recipe from the beginning. If False, any existing
            results will be overwritten by the new simulation. (Default: False).
        report_out: A boolean to indicate whether the recipe progress should be
            displayed in the cmd window (False) or printed (True). Printing can
            be useful for debugging and capturing what's happening in the process
            but recipe reports can often be very long and so it can slow
            Grasshopper slightly. (Default: False).

    Properties:
        * folder
        * workers
        * reload_old
        * report_out
    """
    __slots__ = ('_folder', '_workers', '_reload_old', '_report_out')

    def __init__(self, folder=None, workers=None, reload_old=False, report_out=False):
        """Initialize RecipeSettings."""
        self.folder = folder
        self.workers = workers
        self.reload_old = reload_old
        self.report_out = report_out

    @classmethod
    def from_string(cls, settings_string):
        """Create an RecipeSettings object from a RecipeSettings string."""
        # parse the string representation
        parser = argparse.ArgumentParser()
        parser.add_argument('--folder', action="store", dest="folder")
        parser.add_argument('--workers', action="store", dest="workers", type=int)
        parser.add_argument('--reload-old', action="store_true", default=False)
        parser.add_argument('--report-out', action="store_true", default=False)
        argument_list = shlex.split(settings_string)
        args = parser.parse_args(argument_list)

        # assign the properties
        folder = args.folder if 'folder' in args else None
        workers = int(args.workers) if 'workers' in args else None
        return cls(folder, workers, args.reload_old, args.report_out)

    @property
    def folder(self):
        """Get or set the path to a project folder in which the recipe will be executed.
        """
        return self._folder

    @folder.setter
    def folder(self, value):
        if value is not None:
            value = str(value)
        self._folder = value

    @property
    def workers(self):
        """Get or set a integer the number of CPUs used in the execution of the recipe.

        If set to None, this should be equal to one less than the number of processors
        currently available on the machine.
        """
        return self._workers if self._workers is not None \
            else self._recommended_processor_count()

    @workers.setter
    def workers(self, value):
        if value is not None:
            value = int_in_range(value, mi=1, input_name='recipe workers')
        self._workers = value

    @property
    def reload_old(self):
        """Get or set a boolean for whether existing results should be reloaded."""
        return self._reload_old

    @reload_old.setter
    def reload_old(self, value):
        self._reload_old = bool(value)

    @property
    def report_out(self):
        """Get or set a boolean for whether to print the recipe progress."""
        return self._report_out

    @report_out.setter
    def report_out(self, value):
        self._report_out = bool(value)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    @staticmethod
    def _recommended_processor_count():
        """Get an integer for one minus the number of processors on this machine.

        This method should work on all of the major operating systems and in
        both IronPython and cPython. If, for whatever reason, the number of
        processors could not be sensed, a value of 1 will be returned.
        """
        try:  # assume that we are in cPython
            cpu_count = os.cpu_count()
        except AttributeError:  # we are probably in IronPython
            try:
                from System.Environment import ProcessorCount
                cpu_count = ProcessorCount
            except ImportError:  # no idea what Python this is; let's play it safe
                cpu_count = 1
        return 1 if cpu_count is None or cpu_count <= 1 else cpu_count - 1

    def __copy__(self):
        return RecipeSettings(
            self.folder, self.workers, self.reload_old, self.report_out)

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return (self.folder, self.workers, self.reload_old, self.report_out)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, RecipeSettings) and self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        """RecipeSettings representation."""
        rep_str = '--folder "{}"'.format(self.folder) if self.folder is not None else ''
        rep_str += ' --workers {}'.format(self.workers)
        if self.reload_old:
            rep_str += ' --reload-old'
        if self.report_out:
            rep_str += ' --report-out'
        return rep_str
