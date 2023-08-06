class InternalPfrError(Exception):
    pass


class EmptyScenarioError(InternalPfrError):
    def __init__(self):
        self.message = 'Не был найден сценарий проверки'
