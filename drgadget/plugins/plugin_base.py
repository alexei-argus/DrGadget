class DrGadgetPlugin(object):
    def __init__(self, payload, rop_viewer):
        pass

    # mandatory
    # must return list of tuples
    # (label of menu, callback)
    # or None if no callbacks should be installed
    def get_callback_list(self):
        return None

    def handle_key_down(self, vkey, shift):
        pass

    def run(self):
        pass

    def term(self):
        pass


