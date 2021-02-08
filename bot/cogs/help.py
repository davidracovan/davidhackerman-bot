import discord
from discord.ext import commands
from bot import tools

from bot.cogs.school import School
from bot.cogs.fun import Fun
from bot.cogs.info import Info

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            author = await ctx.guild.fetch_member(688530998920871969)
            embed = tools.create_embed(ctx, 'Bot Commands', desc=f"Written by {author.mention}.")
            embed.add_field(name='Fun Commands', value=f'`{ctx.prefix}help fun`', inline=False)
            embed.add_field(name='Informational Commands', value=f'`{ctx.prefix}help info`', inline=False)
            embed.add_field(name='School Commands', value=f'`{ctx.prefix}help school`', inline=False)
            embed.add_field(name='Link Commands', value=f'`{ctx.prefix}help links`', inline=False)
            embed.add_field(name='Economy Commands', value=f'`{ctx.prefix}help economy`', inline=False)
            await ctx.send(embed=embed)

    @help.command(name='fun')
    async def _fun(self, ctx):
        embed = tools.create_embed(ctx, 'Fun Commands')
        for command in self.bot.get_cog('Fun').get_commands():
            embed.add_field(name=f'{ctx.prefix}{command.name} {command.signature}', value=command.help, inline=False)
        await ctx.send(embed=embed)

    @help.command(name='info')
    async def _info(self, ctx):
        embed = tools.create_embed(ctx, 'Informational Commands')
        for command in self.bot.get_cog('Info').get_commands():
            embed.add_field(name=f'{ctx.prefix}{command.name} {command.signature}', value=command.help, inline=False)
        await ctx.send(embed=embed)

    @help.command(name='school')
    async def _school(self, ctx):
        embed = tools.create_embed(ctx, 'School Commands')
        for command in self.bot.get_cog('School').get_commands():
            embed.add_field(name=f'{ctx.prefix}{command.name} {command.signature}', value=command.help, inline=False)
        await ctx.send(embed=embed)

    @help.command(name='links')
    async def _links(self, ctx):
        embed = tools.create_embed(ctx, 'Link Commands')
        for command in self.bot.get_cog('Links').get_commands():
            embed.add_field(name=f'{ctx.prefix}{command.name} {command.signature}', value=command.help, inline=False)
        await ctx.send(embed=embed)

    @help.command(name='economy')
    async def _economy(self, ctx):
        embed = tools.create_embed(ctx, 'Economy Commands')
        for command in self.bot.get_cog('Economy').get_commands():
            embed.add_field(name=f'{ctx.prefix}{command.name} {command.signature}', value=command.help, inline=False)
        await ctx.send(embed=embed)