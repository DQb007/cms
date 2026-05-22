from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Course, User
from app.schemas import (
    CategoryResponse,
    CourseBatchDeleteRequest,
    CourseBatchDeleteResponse,
    CourseCreate,
    CourseListResponse,
    CourseOut,
    CourseUpdate,
)
from app.security import get_current_user


router = APIRouter(prefix="/api/courses", tags=["courses"])


def _apply_filters(
    statement: Select[tuple[Course]] | Select[tuple[int]],
    code: str | None,
    name: str | None,
    category: str | None,
    price_min: int | None,
    price_max: int | None,
):
    if code:
        statement = statement.where(Course.code.like(f"%{code}%"))
    if name:
        statement = statement.where(Course.name.like(f"%{name}%"))
    if category:
        statement = statement.where(Course.category == category)
    if price_min is not None:
        statement = statement.where(Course.price >= price_min)
    if price_max is not None:
        statement = statement.where(Course.price <= price_max)
    return statement


@router.get("", response_model=CourseListResponse)
def list_courses(
    code: str | None = Query(default=None, max_length=50),
    name: str | None = Query(default=None, max_length=255),
    category: str | None = Query(default=None, max_length=255),
    price_min: int | None = Query(default=None, ge=0),
    price_max: int | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> CourseListResponse:
    base_query = _apply_filters(select(Course), code, name, category, price_min, price_max)
    count_query = _apply_filters(select(func.count()).select_from(Course), code, name, category, price_min, price_max)

    total = db.scalar(count_query) or 0
    items = db.scalars(
        base_query.order_by(Course.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return CourseListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/categories", response_model=CategoryResponse)
def list_categories(db: Session = Depends(get_db)) -> CategoryResponse:
    rows = db.scalars(
        select(Course.category)
        .where(Course.category.is_not(None), Course.category != "")
        .distinct()
        .order_by(Course.category.asc())
    ).all()
    return CategoryResponse(categories=list(rows))


@router.post("", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Course:
    now = datetime.now()
    course = Course(
        code=payload.code,
        name=payload.name,
        url=str(payload.url) if payload.url else None,
        price=payload.price,
        category=payload.category,
        create_time=now,
        creator=current_user.username,
        modify_time=now,
        modifier=current_user.username,
    )
    db.add(course)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="课程编号已存在") from exc
    db.refresh(course)
    return course


@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Course:
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="课程不存在")

    course.code = payload.code
    course.name = payload.name
    course.url = str(payload.url) if payload.url else None
    course.price = payload.price
    course.category = payload.category
    course.modify_time = datetime.now()
    course.modifier = current_user.username
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="课程编号已存在") from exc
    db.refresh(course)
    return course


@router.delete("/batch", response_model=CourseBatchDeleteResponse)
def batch_delete_courses(
    payload: CourseBatchDeleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CourseBatchDeleteResponse:
    del current_user
    unique_ids = list(dict.fromkeys(payload.ids))
    courses = db.scalars(select(Course).where(Course.id.in_(unique_ids))).all()
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到可删除的课程")

    for course in courses:
        db.delete(course)
    db.commit()
    return CourseBatchDeleteResponse(deleted=len(courses))


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="课程不存在")
    db.delete(course)
    db.commit()
