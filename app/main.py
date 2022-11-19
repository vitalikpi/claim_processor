import uuid
from typing import Union, List, Optional

import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
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


class Claim(BaseModel):
    service_date: str
    submitted_procedure: str
    quadrant: Union[str, None] = None
    plan_or_group_no: str
    subscriber_no: str
    provider_npi: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float


class ProcessingResponse(BaseModel):
    uid: str
    net_fee: float


engine = create_engine("mysql+pymysql://root:example@db:3306/claims_db", echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI()


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



