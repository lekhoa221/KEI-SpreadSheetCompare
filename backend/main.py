from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import upload, compare, analyze, sheets

app = FastAPI(title="Spreadsheet Compare AI", version="0.1.0")

# CORS setup for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(upload.router, prefix="/api")
app.include_router(compare.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(sheets.router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Spreadsheet Compare Backend is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
