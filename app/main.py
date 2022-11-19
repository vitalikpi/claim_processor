import uuid
from typing import Union, List, Optional

import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine


class ClaimModel(SQLModel, table=True):
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
    for claim in claims:
        net_fee = claim.provider_fees + claim.member_coinsurance + claim.member_copay - claim.allowed_fees
        result.append(ProcessingResponse(uid=str(uuid.uuid1()), net_fee=net_fee))
    return result



