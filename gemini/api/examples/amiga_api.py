from gemini.api.sensors.amiga import AmigaParser
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
amiga_data_dir = os.path.join(current_dir, "amiga_data", "2024_06_12_19_38_31_521606_moats-unproved.0000.bin")

amiga_parser = AmigaParser()
amiga_parser.parse_file(amiga_data_dir)


# from gemini.api.sensors.amiga import get_events_index, process_file
# import os

# amiga_file = "./gemini/api/examples/amiga_data/2023_09_14_19_06_20_494194_moats-unproved.0000.bin"

# process_file(amiga_file)

