import uuid
from typing import Union, List, Optional
from datetime import date, datetime, time, timedelta

import pymysql
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, validator, NonNegativeFloat
from sqlmodel import Field, Session, SQLModel, create_engine


class ClaimModel(SQLModel, table=True):
    __tablename__ = "claims"

    uid: str = Field(default=None, primary_key=True)
    service_date: str
    submitted_procedure: str
    quadrant: Optional[str] = None
    plan_or_group_no: str
    subscriber_no: str
    provider_npi: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float


"""
Claim information.
"""
class Claim(BaseModel):
    """
    A date when the service was provided
    """
    service_date: date

    """
    A code of submitted procedure. Must always start with 'D'
    """
    submitted_procedure: str = Field(..., min_length=1)

    """
    A quadrant. The only optional field
    """
    quadrant: Union[str, None] = None

    """
    Plan / group #
    """
    plan_or_group_no: str = Field(..., min_length=1)

    """
    Subscriber #
    """
    subscriber_no: str = Field(..., min_length=1)

    """
    Provider NPI
    """
    provider_npi: str = Field(..., min_length=10, max_length=10)

    """
    Provider fees
    """
    provider_fees: NonNegativeFloat

    "Allowed fees"
    allowed_fees: NonNegativeFloat

    """
    Member coinsurance
    """
    member_coinsurance: NonNegativeFloat

    """
    Member copay
    """
    member_copay: NonNegativeFloat

    @validator('submitted_procedure')
    def submitted_procedure_always_starts_with_d(cls, v):
        if v[0] != "D":
            raise ValueError('submitted_procedure must always start with D')
        return v



class ProcessingResponse(BaseModel):
    uid: str
    net_fee: float


engine = create_engine("mysql+pymysql://root:example@db:3306/claims_db", echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI()


"""
Processes and stores list of claims provided in the body.
In response returns a unique id for each claim and it's bet fee.
"""
@app.post("/claim_process")
async def claim_process(claims: List[Claim]) -> ProcessingResponse:
    result = []

    with Session(engine) as session:
        for claim in claims:
            net_fee = claim.provider_fees + claim.member_coinsurance + claim.member_copay - claim.allowed_fees
            uid = str(uuid.uuid1())

            session.add(ClaimModel(
                uid=uid,
                service_date=str(claim.service_date),
                submitted_procedure=claim.submitted_procedure,
                quadrant=claim.quadrant,
                plan_or_group_no=claim.plan_or_group_no,
                subscriber_no=claim.subscriber_no,
                provider_npi=claim.provider_npi,
                provider_fees=claim.provider_fees,
                allowed_fees=claim.allowed_fees,
                member_coinsurance=claim.member_coinsurance,
                member_copay=claim.member_copay
            ))

            result.append(ProcessingResponse(uid=uid, net_fee=net_fee))
        session.commit()
    return result

# 6. Write pseudo code or comments in your code to indicate how **claim_process** will communicate with **payments**.
# There are multiple choices here but propose a reasonable solution based on:
#    - What needs to be done if there is a failure in either service and steps need to be unwinded.
#    - Multiple instances of either service are running concurrently to handle a large volume of claims.
#

# Answer:
# import requests
#
# url = '..../claim_process'
# myobj = [
#   {
#     "service_date": "2022-11-19",
#     "submitted_procedure": "D0180",
#     "plan_or_group_no": "GRP-1000",
#     "subscriber_no": "6546546",
#     "provider_npi": "1497775530",
#     "provider_fees": 80,
#     "allowed_fees": 100,
#     "member_coinsurance": 25,
#     "member_copay": 14.33
#   },
#   {
#     "service_date": "2022-11-19",
#     "submitted_procedure": "D0180",
#     "plan_or_group_no": "GRP-1000",
#     "subscriber_no": "6546546",
#     "provider_npi": "1497775530",
#     "provider_fees": 80,
#     "allowed_fees": 100,
#     "member_coinsurance": 25,
#     "member_copay": 14.33
#   }
# ]'
#
# x = requests.post(url, json = myobj)
#
# - What needs to be done if there is a failure in either service and steps need to be unwinded.
# If failure happens in the claim processor - we should roll back the transaction
# if failure happens in the payment processor - we ahall implement another method to delete the failed claim (or mark them as failed)
#
#  Multiple instances of either service are running concurrently to handle a large volume of claims.
# in this case using of transactions may slow down the DB, I'd recommend marking records as failed or deleting them.










