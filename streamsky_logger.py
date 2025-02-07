import os
import logging
import uuid

script_path = os.path.dirname(os.path.abspath(__file__))

uuid = str(uuid.uuid4().hex)

log = logging.getLogger(__name__)

logging.basicConfig(
    filename=f'{script_path}/logs/{uuid}.log',
    level=logging.INFO
)
