from src.position_writer import PositionWriter
from examples.geobin_writer import parsers

if __name__ == "__main__":
    writer = PositionWriter(parser_module=parsers, commit_interval=20, on_message_threads=5)
    writer.run()