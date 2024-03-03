import os
import datetime

class logger:
    
    file_name = f"./log/{datetime.date.today()}.log"

    # Checking if log file exists. If not, create a new one.
    if not os.path.isfile(file_name) and not os.path.isdir(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            print("Create log file successful.")
            pass

    @staticmethod
    def info(msg: str) -> None:
        logger._log("INFO", msg)

    @staticmethod
    def debug(msg: str) -> None:
        logger._log("DEBUG", msg)

    @staticmethod
    def warning(msg: str) -> None:
        logger._log("WARNING", msg)

    @staticmethod
    def error(msg :str) -> None:
        logger._log("ERROR", msg)

    @staticmethod
    def _log(level: str, msg: str) -> None:
        logger.update_file_name()
        with open(logger.file_name, "a", encoding="utf-8") as f:
            f.writelines(f"{datetime.datetime.now()} {level.upper()}: {msg}\n")
        return

    @staticmethod
    def update_file_name() -> None:
        # An API wrapper for logger._update_file_name()
        logger.file_name = logger._update_file_name()
        return

    @staticmethod
    def _update_file_name() -> str:
        # Automatic rotating file names
        return f"./log/{datetime.date.today()}.log"

def logger_showoff() -> None:
    # Demonstrate the logger
    print(f"Today is {datetime.date.today()}")
    logger.info("something")

if __name__ == "__main__":
    logger_showoff()
