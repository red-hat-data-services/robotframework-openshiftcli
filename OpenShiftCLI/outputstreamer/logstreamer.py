from robot.api import logger

from OpenShiftCLI.outputstreamer import OutputStreamer


class LogStreamer(OutputStreamer):
    def stream(self, output: str, type: str) -> None:
        if type == 'info':
            logger.info(output)
        elif type == "error":
            logger.error(output)
        elif type == "warn":
            logger.warn(output)
