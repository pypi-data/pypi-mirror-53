import logging
from threading import RLock

import typing

from scopeton import compat, glob
from scopeton.objects import Bean
from scopeton.qualifier_tree import QualifierTree
from scopeton.scopeTools import getBean_qualifier, callMethodByName, getClassTree, flatten, ScopetonException

T = typing.TypeVar("T")

class Scope(object):
    '''this is servicelocator pattern implementation'''
    def __init__(self, lock=False, initMethod="postConstruct", destroyMethod="preDestroy", parent=None):
        self._singletons = QualifierTree()
        self._beans = QualifierTree()
        self.lock = lock or RLock()       # type: RLock
        self.initMethod = initMethod
        self.destroyMethod = destroyMethod
        self.parent = parent  #type:  Scope
        self.servicesStarted = False
        self.children = []  # type: typing.List[Scope]
        self.registerInstance(self.__class__, self)
        if parent:
            parent.children.append(self)

    def getInstance(self, name: T) -> T:
        with self.lock:
            return self._getInstance(getBean_qualifier(name))

    def _getInstance(self, qualifier):

        suitableQualifier = self._beans.find_suitable_qualifier(qualifier)

        if self._singletons.contains(suitableQualifier):
            return self._singletons.find_by_qualifier_name(suitableQualifier)

        bean = self._beans.find_by_qualifier_name(suitableQualifier)
        glob.lastScope = self
        if compat.hasInject(bean.cls.__init__):
            instance = bean.cls()
        elif len(compat.getMethodSignature(bean.cls.__init__).args) == 2:
            instance = bean.cls(self)
        elif len(compat.getMethodSignature(bean.cls.__init__).args) > 2:
            raise ScopetonException("Invalid number of parameters for bean constructor, maybe @Inject() decorator forgotten: {}".format(compat.getMethodSignature(bean.cls.__init__).args))
        else:
            instance = bean.cls()

        if bean.singleton:
            self.registerInstance(suitableQualifier, instance)

        return instance

    def registerInstance(self, name, instance):
        qualifier = getBean_qualifier(name)
        suitableQualifier = self._beans.find_suitable_qualifier(qualifier)
        logging.debug("Suitable qualifier for {} is: {}".format(qualifier, suitableQualifier))
        self._singletons.register(suitableQualifier, instance)

    def registerBean(self, *args):
        with self.lock:
            for bean in args:
                if not isinstance(bean, Bean):
                    bean = Bean(bean)
                self._registerBean(bean)

    def remove(self):
        logging.debug("Removing scope: {}".format(self))
        self.stopServices()
        for k in self.children[:]:
            k.remove()
        if self.parent:
            self.parent.children.remove(self)


    def _registerBean(self, bean):
        """
        :type bean: Bean
        """
        for name in bean.qualifier_tree:
            logging.debug("Registering: {} as {}".format(name, bean))
            self._beans.register(name, bean)

    def runServices(self):
        if not self.servicesStarted:
            self.servicesStarted = True
            for bean in self._beans.get_all_objects():
                if bean.service:
                    callMethodByName(self.getInstance(bean), self.initMethod)

            for childScope in self.children:
                childScope.runServices()

    def stopServices(self):
        if self.servicesStarted:
            self.servicesStarted = False
            for bean in self._beans.get_all_objects():
                if bean.service:
                    callMethodByName(self.getInstance(bean), self.destroyMethod)
            for childScope in self.children:
                childScope.stopServices()