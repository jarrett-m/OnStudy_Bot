from __future__ import annotations
from abc import ABC, abstractmethod
import discord


class OSBcmd(ABC):
    """
        Command Patter Interface.
    """

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
