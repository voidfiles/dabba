"""
Module class
"""
from collections import OrderedDict
import copy
import logging

from bunch import Bunch

from dabba.exceptions import ProcessingException, EarlyReturn
from dabba.modules import BaseModule


__all__ = ('BasePipeline', 'Pipeline')

logger = logging.getLogger(__name__)


class DeclarativeModulesMetaclass(type):
    """
    Metaclass that collects Modules declared on the base classes.
    """
    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, BaseModule):
                value.name = key
                current_fields.append((key, value))
                attrs.pop(key)
        current_fields.sort(key=lambda x: x[1].creation_counter)
        attrs['declared_modules'] = OrderedDict(current_fields)

        new_class = (super(DeclarativeModulesMetaclass, mcs)
            .__new__(mcs, name, bases, attrs))

        # Walk through the MRO.
        declared_modules = OrderedDict()
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, 'declared_modules'):
                declared_modules.update(base.declared_modules)

            # Field shadowing.
            for attr in base.__dict__.keys():
                if attr in declared_modules:
                    declared_modules.pop(attr)

        new_class.base_modules = declared_modules
        new_class.declared_modules = declared_modules

        return new_class


class BasePipeline(object):
    # This is the main implementation of all the Pipeline logic. Note that this
    # class is different than Pipeline. See the comments by the Form class for more
    # information. Any improvements to the form API should be made to *this*
    # class, not to the Pipeline class.
    def __init__(self, job=None):
        self.job = job

        # The base_fields class attribute is the *class-wide* definition of
        # modules. Because a particular *instance* of the class might want to
        # alter self.modules, we create self.modules here by copying base_modules.
        # Instances should always modify self.modules; they should not modify
        # self.base_modules.
        self.modules = copy.deepcopy(self.base_modules)

    def process_module(self, module, job):
        return module.process(job)

    def process(self):
        # We could do pre, post hooks if we wanted to here
        job = self.job
        job.modules = []
        job.output = Bunch()

        for name, module in self.modules.iteritems():
            error = None
            job.modules += [name]
            try:
                job = self.process_module(module, job)
            except ProcessingException, e:
                logger.exception('Pipeline %s failed while processing job: %s', self.__class__, self.job)
                error = e
                error_data = e.to_dict()
                error_data['module_name'] = name
            except Exception, e:
                logger.exception('Pipeline %s had an uncontrolled failure while processing job: %s', self.__class__, self.job)
                error = e
                error_data = {
                    'module_name': name,
                    'message': unicode(e),
                    'slug': 'unhandled_exception'
                }

            if error:
                if not job.get('errors'):
                    job.errors = []

                job.errors += [error_data]

                if module.required:
                    raise EarlyReturn('Pipeline failed on a required module', job=job)

        return job


class Pipeline(BasePipeline):
    __metaclass__ = DeclarativeModulesMetaclass
    "A collection of Modules, plus their associated data."
    # This is a separate class from BasePipeline in order to abstract the way
    # self.modules is specified. This class (Form) is the one that does the
    # fancy metaclass stuff purely for the semantic sugar -- it allows one
    # to define a form using declarative syntax.
    # BasePipeline itself has no way of designating self.modules.

