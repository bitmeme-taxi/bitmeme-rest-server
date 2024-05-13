# encoding: utf-8

from fastapi import Path, HTTPException
from pydantic import BaseModel

from server import app, kaspad_client


class BalanceResponse(BaseModel):
    address: str = "btm:qp3gdpw70htp934mmp4fm54sewd23hqjxxshvjpqykw96hlk3nxt5qvgjfpm7"
    balance: int = 38240000000


@app.get("/addresses/{gorAddress}/balance", response_model=BalanceResponse, tags=["BTM addresses"])
async def get_balance_from_kaspa_address(
        gorAddress: str = Path(
            description="BTM address as string e.g. btm:qp3gdpw70htp934mmp4fm54sewd23hqjxxshvjpqykw96hlk3nxt5qvgjfpm7",
            regex="^btm\:[a-z0-9]{61,63}$")):
    """
    Get balance for a given btm address
    """
    resp = await kaspad_client.request("getBalanceByAddressRequest",
                                       params={
                                           "address": gorAddress
                                       })

    try:
        resp = resp["getBalanceByAddressResponse"]
    except KeyError:
        if "getUtxosByAddressesResponse" in resp and "error" in resp["getUtxosByAddressesResponse"]:
            raise HTTPException(status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"])
        else:
            raise

    try:
        balance = int(resp["balance"])

    # return 0 if address is ok, but no utxos there
    except KeyError:
        balance = 0

    return {
        "address": gorAddress,
        "balance": balance
    }
