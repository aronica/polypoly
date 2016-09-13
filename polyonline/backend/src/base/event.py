# -*- coding:utf-8 -*- 

from greenlet import greenlet, getcurrent

class Event(object):
    def __init__(self, name):
        self.name = name
        self.listeners = set()

    def listen(self, listener):
        print '---- in listen'
        print listener
        self.listeners.add(listener)

    def fire(self):
        print '--- in event fire'
        print len(self.listeners)
        for listener in self.listeners:
            listener()

class EventManager(object):
    def __init__(self):
        self.events = {}

    def register(self, name):
        print '---- register'
        self.events[name] = Event(name)

    def fire(self, name):
        print '--- fire ' + name
        print self.events 
        self.events[name].fire()

    def await(self, event_name):
        print '---await ' + event_name
        self.events[event_name].listen(getcurrent().switch)
        print self.events
        getcurrent().parent.switch()

    def use( func):
        return greenlet(func).switch

event_listeners = {}

def fire_event(name):
    event_listeners[name]()

def use_event(func):
    def call(*args, **kwargs):
        generator = func(*args, **kwargs)
        event_name = next(generator)
        def resume():
            try:
                next(generator)
            except StopIteration:
                pass
        event_listeners[event_name] = resume
    return call

