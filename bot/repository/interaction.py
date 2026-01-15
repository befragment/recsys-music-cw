from sqlalchemy.ext.asyncio import AsyncSession

from domain.entity.interaction import Interaction
from repository._orm import InteractionORM


class InteractionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, interaction: Interaction):
        try:
            # Конвертируем доменную сущность в ORM модель
            interaction_orm = InteractionORM(
                user_id=interaction.user_id,
                track_id=interaction.track_id,
                action=interaction.action,
            )
            
            self.session.add(interaction_orm)
            await self.session.commit()
            await self.session.refresh(interaction_orm)
            return interaction
        finally:
            await self.session.close()
