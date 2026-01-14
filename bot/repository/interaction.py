from sqlalchemy.ext.asyncio import AsyncSession


class InteractionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, interaction: Interaction):
        self.session.add(interaction)
        await self.session.commit()
        await self.session.refresh(interaction)
        return interaction