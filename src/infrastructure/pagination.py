from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    pages: int
    per_page: int


def paginate(items: List[T], page: int = 1, per_page: int = 10) -> PaginatedResponse[T]:
    total_items = len(items)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page

    return PaginatedResponse(
        items=items[start:end],
        total=total_items,
        page=page,
        pages=total_pages,
        per_page=per_page,
    )
