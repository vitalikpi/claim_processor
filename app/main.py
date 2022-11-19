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
                service_date=claim.service_date,
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



