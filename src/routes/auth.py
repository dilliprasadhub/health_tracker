from tempfile import template
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from supabase import create_client
from fastapi.responses import RedirectResponse, JSONResponse

from src.config.db import db


router = APIRouter()
templates=Jinja2Templates(directory="templates")



@router.get('/')
def hom():
    return RedirectResponse('/signup')

@router.get('/signup')
def signup(request:Request):
    return templates.TemplateResponse("signup.html",{'request':request})


@router.post('/api/signup')
def api_signup(request:Request, email=Form(...),password=Form(...)):
    result=db.auth.sign_up({
        'email':email,'password':password
    })

    if result:
        return JSONResponse({
            "message":"user created",
            "token":result.session.access_token
        })
    

@router.get('/login')
def login(request:Request):
    return templates.TemplateResponse("login.html",{'request':request})


@router.post('/api/login')
def api_login(request: Request, email=Form(...), password=Form(...)):
    result = db.auth.sign_in_with_password({
        'email': email,
        'password': password
    })

    if result.user:
        response = RedirectResponse('/dashboard',status_code=302)
        response.set_cookie('user_session',result.session.access_token,max_age=3600)
        return response 
    



