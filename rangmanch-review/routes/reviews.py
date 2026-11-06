from fastapi import APIRouter, Depends, Query, HTTPException
from database import get_session

from sqlmodel import Session, func, select
from models import ReviewCreate, Review, ReviewRead, ReviewUpdate


router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewRead)
def create_reviews(review: ReviewCreate, session: Session = Depends(get_session)):
    db_review = Review(**review.model_dump())
    print(f'review: {review}, db_review: {db_review}')
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


@router.get("/", response_model=list[ReviewRead]) # with pagination
def list_reviews(
    play_name: str | None = Query(default=None, description="Filter by play name"),
    session: Session = Depends(get_session), 
    skip: int = Query(default=0, description="Number of records to skip"),
    limit: int = Query(default=10, description="Maximum number of records to return")
    ):
    query = select(Review)
    if play_name:
        query = query.where(Review.play_name == play_name)

    query = query.offset(skip).limit(limit)
    reviews = session.exec(query).all()
    print(reviews, play_name)
    return reviews

@router.get("/average/{play_name}")
def get_avg_rating(
    play_name: str,
    session: Session = Depends(get_session)
):
    avg = session.exec(
        select(func.avg(Review.rating), func.count(Review.id))
        .where(Review.play_name == play_name)
    ).first()
    avg_rating, total_rating = avg

    if total_rating == 0:
        raise HTTPException(status_code=404, detail="No reviews found for this play")
    return {"average_rating": round(avg_rating, 2), "total_rating": total_rating}

@router.get("/play")
def get_all_play(session: Session = Depends(get_session)):
    return session.exec(select(func.distinct(Review.play_name))).all()

@router.get("/{review_id}", response_model=ReviewRead)
def get_review_by_id(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
    

@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    review.rating = review_update.rating
    review.comment = review_update.comment
    session.commit()
    session.refresh(review)
    return review

@router.patch("/{review_id}", response_model=ReviewRead)
def patch_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    update_data = review_update.model_dump(exclude_unset=True)
    review.sqlmodel_update(update_data)
    session.commit()
    session.refresh(review)
    return review

@router.delete("/{review_id}", response_model=ReviewRead)
def delete_review(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return review
