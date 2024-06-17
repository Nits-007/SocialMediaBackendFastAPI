from typing import List, Optional
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from httpx import Limits
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter()

@router.post("/votes", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote , db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)) :

    post  = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"post with {vote.post_id} does not exists")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    found_vote = vote_query.first() 

    if(vote.dir==1) :
        if found_vote : #already found vote(like) :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail=f"user {current_user.id} already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id , user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "Successfully added vote"}
    else :
        if not found_vote :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "Successfully deleted vote"}
