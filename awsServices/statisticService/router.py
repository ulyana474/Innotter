from fastapi import APIRouter
from statisticService.services import get_item, get_table

router = APIRouter(
    tags=["items"],
    responses={404: {"status": "Page not found"}}
)

@router.get('/table')
def table():
    print(get_table())
    return "ok"