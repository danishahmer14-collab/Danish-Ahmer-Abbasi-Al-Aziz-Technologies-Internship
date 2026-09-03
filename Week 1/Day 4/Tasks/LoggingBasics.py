import logging

logging.basicConfig(level=logging.INFO, filename="app.log",
                     format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug("Debug message")     # detailed, dev-only info
logging.info("Info message")       # general events
logging.warning("Warning message") # something unexpected, not fatal
logging.error("Error message")     # a real problem
logging.critical("Critical!")      # serious failure