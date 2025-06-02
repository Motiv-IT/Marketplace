from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.model import DbAdvertisement, DbTransaction, StatusAdvertisementEnum, DbUser
from schemas import TransactionCreate, TransactionRead
from router.auth import read_users_me


router = APIRouter(prefix="/purchase", tags=["Purchase"])


# Dependency: yields a Session and closes it after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/transactions",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED
)
def purchase_advertisement(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(read_users_me)  # ensures only an authorized user can call this
):

    # 1) The buyer is the logged‐in user
    buyer = current_user

    # 2) Check that advertisement exists
    ad = db.query(DbAdvertisement).get(data.advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    # 3) Ensure ad is still OPEN
    if ad.status != StatusAdvertisementEnum.OPEN:
        raise HTTPException(
            status_code=400,
            detail="Advertisement is not available for sale"
        )

    # 4) Prevent self‐purchase
    if ad.user_id == buyer.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot purchase your own advertisement"
        )

    # 5) Derive seller_id from the advertisement’s owner
    seller_id = ad.user_id

    # 6) Create the Transaction, using current_user.id as buyer_id
    new_tx = DbTransaction(
        buyer_id=buyer.id,
        seller_id=seller_id,
        advertisement_id=data.advertisement_id,
        completed=data.completed
    )
    db.add(new_tx)

    # 7) Mark the advertisement as SOLD so it can’t be purchased again
    ad.status = StatusAdvertisementEnum.SOLD

    # 8) Commit & refresh
    db.commit()
    db.refresh(new_tx)

    return new_tx