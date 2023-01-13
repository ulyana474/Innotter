import json
import logging
from decimal import Decimal
from fastapi import FastAPI, Request, HTTPException
from statisticService.controllers import get_statistics


# https://stackoverflow.com/questions/63278737/object-of-type-decimal-is-not-json-serializable
class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

app = FastAPI()


@app.get("/statistics")
def get_stat(request: Request):
    LOGGER.info(request.query_params)
    page_id = int(request.query_params.get("id", "-1"))
    if page_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    response = get_statistics(page_id)
    item = json.dumps(response.get("Item", {}), cls=DecimalEncoder)
    return item
