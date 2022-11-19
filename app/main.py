from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel

import uuid


class Claim(BaseModel):
    service_date: str
    submitted_procedure: str
    quadrant: Union[str, None] = None
    plan_or_Group_no: str
    subscriber_no: str
    provider_npi: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float


class ProcessingResponse(BaseModel):
    uid: str
    net_fee: float


app = FastAPI()


@app.post("/claim_process")
async def claim_process(claims: List[Claim]) -> ProcessingResponse:
    result = []
    for claim in claims:
        net_fee = claim.provider_fees + claim.member_coinsurance + claim.member_copay - claim.allowed_fees
        result.append(ProcessingResponse(uid=str(uuid.uuid1()), net_fee=net_fee))
    return result



