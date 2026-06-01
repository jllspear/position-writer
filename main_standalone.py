from src.position_writer import PositionWriter

if __name__ == "__main__":
    writer = PositionWriter(
        parser_module=None, commit_interval=3, on_message_threads=8
    )
    writer.run()