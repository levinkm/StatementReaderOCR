from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.utils.rabbitmq import consume_from_rabbitmq
from routers import statements
from database import Engine
import models.models as models
from config.settings import DEBUG,ORIGINS


# to create all the tables using the already defined schema
# models.Base.metadata.create_all(bind=Engine)

app = FastAPI(debug=DEBUG, title="Fedhatrac OCR API", version="0.1.0")


@app.on_event("startup")
async def startup_event():
   return consume_from_rabbitmq("bank_statements")

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(statements.router)




@app.get("/")
async def root():
    return {"message": "Hello World"}
