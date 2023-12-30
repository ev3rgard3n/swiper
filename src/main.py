from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.config import DATABASE_URL
from src.auth.router import router as auth_router


app = FastAPI(title="Swiper")

app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
async def qwerr():
    html_content = """
    <html>
        <head>
            <title>Ya pomnu penis bolshoy</title>
        </head>
        <body>
            <h1><a href='http://127.0.0.1:8000/docs'>docs</a></h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
