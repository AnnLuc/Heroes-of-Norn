# app/routes/campaigns.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, schemas  # Импортируем схемы

from fastapi.security import OAuth2PasswordRequestForm
from app.models.database import get_db
from app.schemas.campaign import CampaignCreate, CampaignOut
from app.crud import crud_campaign
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.user import UserOut
from app.crud import crud_character

router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"]
)

templates = Jinja2Templates(directory="app/templates")

# Путь для получения списка кампаний
@router.get("/", response_class=HTMLResponse)
def read_campaigns(request: Request, db: Session = Depends(get_db)):
    """
    Получение списка всех кампаний.

    :param request: Запрос для передачи в шаблон
    :param db: Сессия базы данных
    :return: Ответ с HTML-шаблоном списка кампаний
    """
    campaigns = crud_campaign.get_all_campaigns(db)
    return templates.TemplateResponse("campaigns/list.html", {
        "request": request, "campaigns": campaigns
    })

# Путь для логина
@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Обработчик логина пользователя.

    :param request: Запрос для передачи в шаблон
    :param form_data: Данные формы для логина
    :return: Ответ с перенаправлением или ошибкой
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request, "message": "Неверные данные"
        })
    response = RedirectResponse(url="/campaigns", status_code=302)
    return response

# Форма создания кампании (GET)
@router.get("/create", response_class=HTMLResponse)
def create_campaign_form(request: Request):
    """
    Отображение формы для создания кампании.

    :param request: Запрос для передачи в шаблон
    :return: Ответ с формой для создания кампании
    """
    return templates.TemplateResponse("campaigns/create.html", {"request": request})

# Обработчик для создания кампании (POST)
@router.post("/create", response_class=HTMLResponse)
def create_campaign_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Обработчик для создания кампании.

    :param request: Запрос для передачи в шаблон
    :param name: Название кампании
    :param description: Описание кампании
    :param db: Сессия базы данных
    :return: Ответ с перенаправлением на список кампаний или ошибкой
    """
    gm_id = 1  # Замените на ID текущего пользователя, если нужно
    campaign_data = CampaignCreate(name=name, description=description)
    try:
        crud_campaign.create_campaign(db, campaign_data, gm_id)
        return RedirectResponse(url="/campaigns/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при создании кампании: {e}")

# Обработчик для создания кампании с авторизацией (POST)
@router.post("/create-auth", response_model=CampaignOut)
async def create_campaign_route(
    name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обработчик для создания кампании с авторизацией.

    :param name: Название кампании
    :param description: Описание кампании
    :param db: Сессия базы данных
    :param current_user: Текущий авторизованный пользователь
    :return: Созданная кампания
    """
    campaign = CampaignCreate(name=name, description=description)
    try:
        return crud_campaign.create_campaign(db=db, campaign=campaign, gm_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при создании кампании: {str(e)}")

# Путь для получения подробностей о кампании
@router.get("/{campaign_id}", response_class=HTMLResponse)
def campaign_detail(campaign_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Получение подробной информации о кампании по ID.

    :param campaign_id: ID кампании
    :param request: Запрос для передачи в шаблон
    :param db: Сессия базы данных
    :return: Ответ с HTML-шаблоном подробностей кампании
    """
    campaign = crud_campaign.get_campaign_by_id(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Кампания не найдена")
    characters = crud_character.get_characters_by_campaign_id(db, campaign_id)
    return templates.TemplateResponse("campaigns/detail.html", {
        "request": request, "campaign": campaign, "characters": characters
    })
