

class BaseModule(object):
    # Tracks each time a Module instance is created. Used to retain order.
    creation_counter = 0
    default_input_key = None
    defauly_output_key = None

    def __init__(self, name=None, required=True):
        self.name = name
        self.required = required

        # Increase the creation counter, and save our local copy.
        self.creation_counter = BaseModule.creation_counter
        BaseModule.creation_counter += 1

    def process(self, job):
        return job