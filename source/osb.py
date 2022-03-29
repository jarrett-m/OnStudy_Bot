from discord.ext import commands
import osb_commands as cmd
import discord


class OSB(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)
        self.bot_commands()
        self.cmds = {'ping': cmd.Ping(),
                     'add': cmd.Add(),
                     'remove': cmd.Remove()
                     }
        self.perm_num = 1071698665025

    def bot_commands(self):
        @self.command(name="ping")
        async def ping(ctx):
            await self.cmds['ping'].execute(ctx)

        @self.command(name="add")
        async def add(ctx, role: discord.Role):
            await self.cmds['add'].execute(ctx, self.perm_num, role)

        @self.command(name="remove")
        async def remove(ctx, role):
            await self.cmds['remove'].execute(ctx, self.perm_num, role)


bot = OSB(command_prefix="!")
bot.run("OTU3ODg1MTU0ODY3NzAzODU4.YkFSEQ.oUVaPo5zzoaQ4QAAD8sXCXBgIis")
