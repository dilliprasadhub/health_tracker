
from tempfile import template
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from streamlit import user
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse

from src.config.db import db
from utils import get_loggedin_user


router = APIRouter()
templates=Jinja2Templates(directory="templates")


  

@router.get('/dashboard')
def dashboard(request:Request):
    user = get_loggedin_user(request)

    if user : 
        result = db.table('health_tracker').select ('*') .eq('user_id',user.id).execute()
        
        
        return templates.TemplateResponse("dashboard.html",{'request':request,'details':result.data})
    return RedirectResponse('/login')


    
    
