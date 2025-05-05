"""Маршруты для работы с персонажами."""

from typing import List
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.character import Character, CharacterCreate, CharacterUpdate
from app.crud import crud_character
from app.models.models import Attribute, Skill, CharacterAttribute, CharacterSkill

router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_model=List[Character])
def get_characters(db: Session = Depends(get_db)):
    """Получение всех персонажей."""
    return crud_character.get_characters(db)


@router.post("/", response_model=Character)
def create_character(character_data: CharacterCreate, db: Session = Depends(get_db)):
    """Создание нового персонажа."""
    user_id = 1  # TODO: заменить на Depends(current_user)
    campaign_id = 1  # TODO: заменить на Depends(campaign_context)
    return crud_character.create_character(db, character_data, user_id, campaign_id)


@router.put("/{character_id}", response_model=Character)
def update_character(character_id: int, character_data: CharacterUpdate, db: Session = Depends(get_db)):
    """Обновление существующего персонажа."""
    character = crud_character.update_character(db, character_id, character_data)
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    return character


@router.delete("/{character_id}", response_model=Character)
def delete_character(character_id: int, db: Session = Depends(get_db)):
    """Удаление персонажа по ID."""
    character = crud_character.delete_character(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    return character


@router.get("/roll/{character_id}/{attribute}/{skill}", response_model=int)
def roll_for_attribute_and_skill(character_id: int, attribute: str, skill: str, db: Session = Depends(get_db)):
    """Выполнение броска по атрибуту и навыку."""
    character = crud_character.get_character_by_id(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    return crud_character.roll_attribute(character, attribute, skill)


@router.get("/attributes_and_skills")
def get_attributes_and_skills(db: Session = Depends(get_db)):
    """Получение всех атрибутов и сгруппированных по ним навыков."""
    attributes = db.query(Attribute).all()
    skills = db.query(Skill).all()

    grouped_skills = {attr.name: [] for attr in attributes}
    for skill in skills:
        grouped_skills[skill.attribute.name].append(skill)

    return {"attributes": attributes, "grouped_skills": grouped_skills}


@router.get("/create/{campaign_id}", response_class=HTMLResponse)
async def create_character_form(request: Request, campaign_id: int, db: Session = Depends(get_db)):
    """Форма для создания нового персонажа."""
    attributes = db.query(Attribute).all()
    skills = db.query(Skill).all()

    grouped_skills = {attr.name: [] for attr in attributes}
    for skill in skills:
        grouped_skills[skill.attribute.name].append(skill)

    return templates.TemplateResponse("characters/create.html", {
        "request": request,
        "attributes": attributes,
        "grouped_skills": grouped_skills,
        "campaign_id": campaign_id
    })


@router.post("/create", response_class=HTMLResponse)
async def create_character_post(request: Request, db: Session = Depends(get_db)):
    """Обработка формы создания персонажа."""
    form = await request.form()
    name = form.get("name")
    description = form.get("description")
    campaign_id = int(form.get("campaign_id"))
    user_id = 1  # TODO: заменить на Depends(current_user)

    attributes = {
        int(k[len("attributes["):-1]): int(v)
        for k, v in form.items() if k.startswith("attributes[")
    }
    skills = {
        int(k[len("skills["):-1]): int(v)
        for k, v in form.items() if k.startswith("skills[")
    }

    character_data = CharacterCreate(
        name=name,
        description=description,
        attributes=attributes,
        skills=skills
    )
    crud_character.create_character(db, character_data, user_id, campaign_id)
    return RedirectResponse(url=f"/campaigns/{campaign_id}", status_code=303)


@router.get("/{character_id}", response_class=HTMLResponse)
async def character_detail(character_id: int, request: Request, db: Session = Depends(get_db)):
    """Детализация персонажа."""
    character = crud_character.get_character_by_id(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    char_attr_values = {ca.attribute.name: ca.value for ca in character.attributes}
    char_skill_values = {cs.skill.name: cs.bonus for cs in character.skills}

    all_skills = db.query(Skill).all()
    grouped_skills = defaultdict(list)
    for skill in all_skills:
        grouped_skills[skill.attribute.name].append(skill)

    attribute_names = [attr.name for attr in db.query(Attribute).all()]

    return templates.TemplateResponse("characters/detail.html", {
        "request": request,
        "character": character,
        "attribute_names": attribute_names,
        "grouped_skills": dict(grouped_skills),
        "char_attr_values": char_attr_values,
        "char_skill_values": char_skill_values
    })


@router.get("/{character_id}/edit", response_class=HTMLResponse)
async def edit_character(request: Request, character_id: int, db: Session = Depends(get_db)):
    """Форма редактирования персонажа."""
    character = crud_character.get_character_by_id(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    attributes = db.query(Attribute).all()
    skills = db.query(Skill).all()
    grouped_skills = {attr.name: [] for attr in attributes}
    for skill in skills:
        grouped_skills[skill.attribute.name].append(skill)

    char_attr_values = {
        ca.attribute.name: ca.value
        for ca in db.query(CharacterAttribute).filter_by(character_id=character_id).all()
    }
    char_skill_values = {
        cs.skill.name: cs.bonus
        for cs in db.query(CharacterSkill).filter_by(character_id=character_id).all()
    }

    return templates.TemplateResponse("characters/edit.html", {
        "request": request,
        "character": character,
        "attributes": attributes,
        "grouped_skills": grouped_skills,
        "char_attr_values": char_attr_values,
        "char_skill_values": char_skill_values
    })


@router.post("/{character_id}", response_class=HTMLResponse)
async def edit_character_post(request: Request, character_id: int, db: Session = Depends(get_db)):
    """Обработка формы редактирования персонажа."""
    form_data = await request.form()
    name = form_data.get("name")
    description = form_data.get("description")

    attributes = {
        int(k[len("attributes["):-1]): int(v)
        for k, v in form_data.items() if k.startswith("attributes[")
    }
    skills = {
        int(k[len("skills["):-1]): int(v)
        for k, v in form_data.items() if k.startswith("skills[")
    }

    character = crud_character.get_character_by_id(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    character.name = name
    character.description = description

    for attribute_id, value in attributes.items():
        attr = db.query(CharacterAttribute).filter_by(character_id=character_id, attribute_id=attribute_id).first()
        if attr:
            attr.value = value
        else:
            db.add(CharacterAttribute(character_id=character_id, attribute_id=attribute_id, value=value))

    for skill_id, bonus in skills.items():
        skill = db.query(CharacterSkill).filter_by(character_id=character_id, skill_id=skill_id).first()
        if skill:
            skill.bonus = bonus
        else:
            db.add(CharacterSkill(character_id=character_id, skill_id=skill_id, bonus=bonus))

    db.commit()

    return RedirectResponse(url=f"/characters/{character_id}", status_code=303)

