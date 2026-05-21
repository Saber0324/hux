import traceback
from typing import Self
import discord
from discord.ui.select import BaseSelect

from templates.embeds import correctUsageEmbed


class BaseView(discord.ui.View):
    interaction: discord.Interaction | None = None
    message: discord.Message | None = None

    def __init__(
        self, user: discord.User | discord.Member, timeout: float = 60.0
    ) -> None:
        super().__init__(timeout=timeout)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "Only the user that invoked the command can interact with this view.",
                ephemeral=True,
            )
            return False
        self.interaction = interaction
        return True

    def _disable_all(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button) or isinstance(item, BaseSelect):
                item.disabled = True

    async def _edit(self, **kwargs) -> None:
        if self.interaction is None and self.message is not None:
            await self.message.edit(**kwargs)
        elif self.interaction is not None:
            try:
                await self.interaction.response.edit_message(**kwargs)
            except discord.InteractionResponded:
                await self.interaction.edit_original_response(**kwargs)

    async def on_error(
        self,
        _: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[Self],
    ) -> None:
        tb = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        message = f"An error ocurred while processing the interaction for {str(item)}:\n```py\n{tb}\n```"
        self._disable_all()
        await self._edit(content=message, view=self)
        self.stop()

    async def on_timeout(self) -> None:
        self._disable_all()
        await self._edit(view=self)


class CorrectUsageMenu(BaseView):
    LANGS = ["Python", "Go", "Brainfuck"]

    @discord.ui.select(
        cls=discord.ui.Select,
        options=[discord.SelectOption(label=lang) for lang in LANGS],
        placeholder="Select a language.",
        min_values=1,
        max_values=1,
    )
    async def select(
        self, interaction: discord.Interaction, select: discord.ui.Select[Self]
    ) -> None:
        await interaction.response.defer()
        await interaction.followup.send(embed=correctUsageEmbed(select.values[0]))
        self._disable_all()
        await self._edit(view=self)
