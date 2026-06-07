from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message:str="success",data:dict=None):
    content={
        "code":200,
        "message":message,
        "data":data
    }
    # 将字典转为json
    return JSONResponse(content=jsonable_encoder( content))