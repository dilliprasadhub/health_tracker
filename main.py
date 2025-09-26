from fastapi import FastAPI
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from src.routes.auth import router as auth_router
from src.routes.dashboard import router as dashboard_router
from src.routes.details import router as add_deatils_router



app=FastAPI()
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(add_deatils_router)

