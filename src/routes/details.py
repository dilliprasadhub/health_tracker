from tempfile import template
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse

from utils import get_loggedin_user


from src.config.db import db


router = APIRouter()
templates=Jinja2Templates(directory="templates")


@router.get('/add/details')
def new_details(request:Request):
    user = get_loggedin_user(request)
    if user : 
        return templates.TemplateResponse("Add_details.html",{'request':request})
    return RedirectResponse('/login')



@router.post('/add/details')
def create_details(request:Request,
                   date = Form(...),
                   steps=Form(...),
                   water=Form(...),
                   sleep=Form(...),
                   weight=Form(...),
                   activity=Form(...),
                   notes=Form(...)  
                   ):
    user= get_loggedin_user(request)
    if user :
        result = db.table('health_tracker').insert({
                'user_id':user.id,
                'Date':date,
                'Steps':steps,
                'Water':water,
                'Sleep':sleep,
                'Weight':weight,
                'Activity':activity,
                'Notes':"nothing"
            }).execute()
        if result.data:
            return RedirectResponse('/dashboard',status_code=302) 
            
            


        