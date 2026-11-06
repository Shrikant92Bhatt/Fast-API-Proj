# A D2C brand needs to auto-fill city and state fields when a customer types their pincode during checkout. This reduces friction and typos in the address form.

from fastapi import FastAPI
import uvicorn

from data import pincode_db
from exceptions import PinCodeNotFoundError,InvalidPinCodeError, invalid_pin_code_handler ,pincode_not_found_handler
from models import LocationResponse, PincodeRequest, BulkResponse, BulkRequest

app = FastAPI(
    title="Auto fill city by pin",
    description="utility to auto fill city and state from pin code"
)

# Register you exception Handler 
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pin_code_handler)

@app.get("/")
def root():
    return {
        "message": "Pincode lookup api"
    }

@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pin(code: str):
    if len(code)  != 6 or not code.isdigit():
        raise InvalidPinCodeError(code, "Pincode must be 6 digit")
    if code not in pincode_db:
        raise PinCodeNotFoundError(code)
    
    return pincode_db[code]

@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request:BulkRequest):
    result=[]
    missing=[]
    for code in request.pincodes:
        if code in pincode_db:
            result.append(pincode_db[code])
        else:
            missing.append(code)
    
    return BulkResponse(
        missing=missing,
        result=result,
        found=len(result),
        not_found=len(missing)
    )

@app.post("/lookup", response_model=LocationResponse)
def lookup_pincode(request: PincodeRequest):
    location = pincode_db.get(request.pincode)
    if location is None:
        raise PinCodeNotFoundError(request.pincode)
    return location


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)