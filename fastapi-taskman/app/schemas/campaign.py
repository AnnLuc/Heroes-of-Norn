# app/schemas/campaign.py

from pydantic import BaseModel

# Модели для работы с кампаниями.
# Этот модуль включает схемы для создания, обновления и вывода информации о кампаниях.

class CampaignBase(BaseModel):
    """
    Базовая модель для кампании.
    Включает имя и описание кампании.
    """
    name: str
    description: str  # Сделаем описание необязательным

class CampaignCreate(BaseModel):
    """
    Модель для создания кампании.
    Включает имя и описание кампании.
    """
    name: str
    description: str

class Campaign(CampaignBase):
    """
    Модель кампании.
    Включает идентификатор кампании и идентификатор гейм-мастера.
    """
    id: int
    gm_id: int

    class Config:
        """
        Конфигурация для работы с аттрибутами модели в Pydantic V2.
        """
        from_attributes = True

class CampaignOut(CampaignBase):
    """
    Модель для вывода информации о кампании.
    Включает идентификатор кампании, идентификатор гейм-мастера и описание.
    """
    id: int
    gm_id: int
    description: str

    class Config:
        """
        Конфигурация для работы с аттрибутами модели в Pydantic V2.
        """
        from_attributes = True

