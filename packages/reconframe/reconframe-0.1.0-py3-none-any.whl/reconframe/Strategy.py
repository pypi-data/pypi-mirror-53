from .Helpers import brief
from .Intel import *
import re


class Offensive():
    """Single plan, with everything. Like single threaded bruteforcing"""
    def __init__(self, plan, economy={}, security={}, iterations=1):
        self.strategy = Strategy()
        self.strategy.set_plan('plan_a', plan)
        self.iterations = iterations

    def execute(self):
        for x in range(0, self.iterations):
            brief(self.strategy.main())


class Mass():
    """A wrapper for thread object for running plans as per Economy or default Economy. Best for harvesting"""
    pass


class Economy():
    """Controls how much resources must be used in a plan execution."""
    pass


class Maneuver():
    """Linked list for strategies. Returns a group of intel"""
    pass


class Unity():
    """Parse all the intel captured by running plans into a single intel"""
    pass


class Security():
    """Security Policy that implements safer "Economy" to maintain safety measures of the attacker"""
    pass


def plan(func):
    def decorator():
        return information(func())              # ensure plan always ends up with an information

    return decorator


class Strategy():
    def __init__(self, economy={}, security={}):
        self.economy = economy
        self.security = security
        self.plans = {}

    def main(self):
        keys = sorted(self.plans, key=lambda plan: self.plans[plan]['must_run'])
        intels = []
        for key in keys:
            intels.append(self.plans[key]['plan']())
        
        return intels
        

    def get_plan(self, plan_id):
        try:
            return self.plans['plan_id']
        except KeyError:
            return False

    def set_plan(self, plan_id, plan, override=False):
        if(not callable(plan)):
            raise Exception("Plan must be a callable function!")

        if(not override):
            try:
                self.plans[plan_id]
                raise Exception("Plan already exists!")
            except KeyError:
                pass

        self.plans[plan_id] = {'plan': plan, 'must_run': 100}
        return True
