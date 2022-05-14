init -2 python:
    class Infraction(renpy.store.object):
        #These are common infractions that may be used throughout the game
        @staticmethod
        def bureaucratic_mistake_factory(name = "Bureaucratic Mistake", desc = None, severity = 1, days_valid = 3):
            if desc is None:
                desc = "Failure to dot all i's and cross all t's. It's impossible to do anything right here!"
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def underperformance_factory(name = "Underperformance", desc = None, severity = 1, days_valid = 7):
            if desc is None:
                desc = "Work performance lower than expected of the employee."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def careless_accident_factory(name = "Careless Accident", desc = None, severity = 2, days_valid = 7):
            if desc is None:
                desc = "Damage to company equipment or waste of company supplies due to a careless mistake."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def office_disturbance_factory(name = "Workplace Disturbance", desc = None, severity = 2, days_valid = 7):
            if desc is None:
                desc = "Actions that have upset the normal peace and quiet of the office."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def out_of_uniform_factory(name = "Out of Uniform", desc = None, severity = 3, days_valid = 7):
            if desc is None:
                desc = "Failure to wear a company mandated uniform."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def disobedience_factory(name = "Disobedience", desc = None, severity = 3, days_valid = 7):
            if desc is None: #Not in the parameters to keep things a little tidier.
                desc = "Intentional disregard of a direct order order or instruction."
            return Infraction(name, desc, severity, days_valid)

        @staticmethod
        def inappropriate_behaviour_factory(name = "Inappropriate Behaviour", desc = None, severity = 3, days_valid = 7):
            if desc is None:
                desc = "Actions inappropriate for a workplace setting. Strange how this never applies to the management..."
            return Infraction(name, desc, severity, days_valid)

        def __init__(self, name, desc, severity, days_valid, days_existed = 0):
            self.name = name #The name of the infraction, as might show up on a menu
            self.desc = desc #A short, two or three sentence explanation for what the infraction is, for tooltip purposes.
            self.severity = severity #An int from 1 (least severe) to 5 (most severe). Punishments are gated by the severity of the infraciton
            if strict_enforcement.is_active():
                self.severity += 1
            if draconian_enforcement.is_active():
                self.severity += 1

            self.days_valid = days_valid #How many days from the creation of the infraction it is valid to punish someone for
            self.days_existed = days_existed #How long this infraction has existed on someone.
