from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, Tuple
import discord
from difflib import get_close_matches
from disputils import BotMultipleChoice

class OSBcmd(ABC):
    """
        Command Patter Interface.
    """

    @abstractmethod
    async def execute(self, **kwargs):
        pass


class Ping(OSBcmd):
    """
    A simple ping command.
    """

    async def execute(self, ctx) -> None:
        await ctx.send("pog")


class Add(OSBcmd):
    """
    Allows users to add themselves to a role.
    Users can only add themselves to roles that have a certian permission number.
    This is so users cannot add themselves to any admin groups, by default I've made the
    permission number the default new role number found in osb.py but this can easily be changed.
    """

    async def execute(self, ctx, perm_num, role: discord.Role) -> None:
        user = ctx.message.author
        if role is None:
            await ctx.send(f'That role dose not exist {user.mention}')
        elif role.permissions.value != perm_num:
            await ctx.send('You do not have permission to add this role')
        elif role in user.roles:
            await ctx.send(f"You cannot add a role you already have {user.mention}")
        else:
            user = ctx.message.author
            await user.add_roles(role)
            await ctx.send(f'Added {role} to {user.mention}')


class Remove(OSBcmd):
    """
    Allows users to remove themselves to a role (that has a certain permission number).
    """

    async def execute(self, ctx, perm_num, role) -> None:
        role = discord.utils.get(ctx.guild.roles, name=role)
        user = ctx.message.author
        if role is None:
            await ctx.send(f'That role dose not exist {user.mention}')
        elif role.permissions.value != perm_num:
            await ctx.send('You do not have permission to remove this role')
        elif role not in user.roles:
            await ctx.send(f"You cannot remove a role you don't have {user.mention}")
        else:
            await user.remove_roles(role)
            await ctx.send(f"Removed {role} from {user.mention}")


class Search:
    """
    Allow users to search courses, and add themseleves using a choice box.
    """
    async def execute(self, ctx, perm_number, role):
        user = ctx.message.author
        roles = ctx.guild.roles
        roles = [i for i in roles if i.permissions.value == perm_number and i.name != '@everyone']
        role_names = get_close_matches(role, [i.name for i in roles])

        if not role_names:
            await ctx.send(f"Could not find any roles close to that name... {user.mention}")
            return None

        multiple_choice = BotMultipleChoice(ctx, role_names, "Search Results:")
        choice = await multiple_choice.run()
        choice = choice[0]
        if choice:
            for i in roles:
                if choice == i.name:
                    choice = i
                    break
        else:
            await multiple_choice.quit(f"Sorry you did not see the class you were looking for {user.mention}!")
            return None

        await multiple_choice.quit()
        return choice
