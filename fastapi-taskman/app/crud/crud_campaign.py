# app/crud/crud_campaign.py
from sqlalchemy.orm import Session
from app.models.models import Campaign
from app.schemas.campaign import CampaignCreate, CampaignOut
from app.schemas.character import CharacterOut

# Модуль для работы с кампаниями (CRUD операции)

def create_campaign(db: Session, campaign: CampaignCreate, gm_id: int):
    """
    Создаёт новую кампанию в базе данных.

    :param db: Сессия базы данных
    :param campaign: Данные для создания кампании
    :param gm_id: ID ведущего кампании
    :return: Созданная кампания
    """
    if not campaign.description:  # Проверка обязательности description
        raise ValueError("Описание кампании обязательно")
    
    db_campaign = Campaign(
        name=campaign.name,
        description=campaign.description,  # Сохраняем описание
        gm_id=gm_id  # gm_id передаем здесь
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


def get_campaign_by_id(db: Session, campaign_id: int):
    """
    Получает кампанию по ID.

    :param db: Сессия базы данных
    :param campaign_id: ID кампании
    :return: Данные кампании или None, если не найдено
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if campaign:
        return CampaignOut(
            id=campaign.id,
            name=campaign.name,
            gm_id=campaign.gm_id,
            characters=[CharacterOut(id=char.id, name=char.name) for char in campaign.characters],
            description=campaign.description  # добавляем описание
        )
    return None

def get_all_campaigns(db: Session):
    """
    Получает все кампании.

    :param db: Сессия базы данных
    :return: Список всех кампаний
    """
    campaigns = db.query(Campaign).all()
    return [
        CampaignOut(
            id=campaign.id,
            name=campaign.name,
            gm_id=campaign.gm_id,
            characters=[CharacterOut(id=char.id, name=char.name) for char in campaign.characters],
            description=campaign.description  # добавляем описание
        )
        for campaign in campaigns
    ]
