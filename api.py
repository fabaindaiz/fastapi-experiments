from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import src.parameter as parameter
import src.wrapper as wrapper


app = FastAPI(title="Test API",
              version="1.0.0",
              docs_url= "/docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parameter.router)
app.include_router(wrapper.router)
