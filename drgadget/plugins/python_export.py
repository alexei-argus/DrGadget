from plugin_base import DrGadgetPlugin
import idc
import traceback


class PythonExport(DrGadgetPlugin):
    def __init__(self, payload, rop_viewer):
        super(PythonExport, self).__init__(payload, rop_viewer)

        self.payload = payload
        self.rop_viewer = rop_viewer
        self.menucallbacks = [("Export ROP to Python", self.run, "Ctrl-P")]

    # mandatory
    # must return list of tuples
    # (label of menu, callback)
    # or None if no callbacks should be installed
    def get_callback_list(self):
        return self.menucallbacks

    def handle_key_down(self, vkey, shift):
        # Ctrl-P
        if vkey == ord('P') and shift == 4:
            self.run()

    def run(self):
        file_name = idc.AskFile(1, "*.py", "Export ROP to Python")

        if not file_name:
            return

        try:
            with open(file_name, 'w') as f:
                f.write('''rop_buffer = ""\n''')
                pointer_pack_format_string = self.payload.proc.get_ptr_pack_fmt_string()
                pointer_format_string = "0x" + self.payload.proc.get_data_fmt_string()

                previous_block_number = None
                block_counter = 0

                for index, item in enumerate(self.payload.items):
                    if item.block_num != previous_block_number:
                        f.write("# block %d\n" % block_counter)
                        block_counter += 1
                        previous_block_number = item.block_num

                    line = '''rop_buffer += struct.pack("%s", %s)''' % (pointer_pack_format_string,
                                                                        pointer_format_string % item.ea)
                    if len(item.comment) > 0:
                        line += ("  # %s" % item.comment)

                    f.write(line)
                    f.write('\n')
        except:
            traceback.print_exc()
            return

        print "payload exported to %s" % file_name

    def term(self):
        pass
