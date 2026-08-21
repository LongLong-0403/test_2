from fastapi import FastAPI , Depends , HTTPException , Request
from fastapi.responses import JSONResponse
from db.database import Base , engine , get_db 
import models
from sqlalchemy.orm import Session
from sqlalchemy import text
from routers import auth , users_router , club_router



Base.metadata.create_all(bind = engine)
app = FastAPI(title="Student Club Management API")


@app.exception_handler(HTTPException)
async def http_exception_handle(request:Request ,exc:HTTPException): 
    return JSONResponse(
        status_code=exc.status_code , 
        content={
            "success" : False , 
            "status_code": exc.status_code , 
            "message" : exc.detail
        }
    )


@app.get("/health")
def health_check(db : Session = Depends(get_db)): 
    db.execute(text("SELECT 1"))
    return {
        "status": "Oke bro hahaha",
        "message": "API chạy ngon đấy hahaha"
    }

app.include_router(auth.router)
app.include_router(users_router.router)
app.include_router(club_router.router)