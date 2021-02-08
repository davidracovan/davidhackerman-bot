import discord
from discord.ext import commands
from bot import tools

class Games(commands.Cog):
    BOARDS = []
    def __init__(self, bot):
        self.bot = bot

    def create_ttt_board(self, ctx, player2):
        board = {"board": [["", "", ""], ["", "", ""], ["", "", ""]]}
        board["server_id"] = ctx.guild.id
        board["player1"] = ctx.message.author.id
        board["player2"] = player2.id

        
    """┌───┬───┬───┐
    │ X │   │   │
    ├───┼───┼───┤
    │   │   │   │
    ├───┼───┼───┤
    │   │   │   │
    └───┴───┴───┘"""

    # @commands.group()
    # async def start(self, ctx):
    #     if ctx.invoked_subcommand is None:
    #         desc = 'You need to specify a game to start.'
    #         embed = create_embed(ctx, 'Start Game', description=desc)
    #         await ctx.send(embed=embed)
    
    @commands.command(aliases=['tic', 'tac', 'toe', 'ttt'])
    async def tictactoe(self, ctx, player2: discord.User):

        def check(msg):
            return msg.author == player2 and msg.channel == ctx.channel and \
            msg.content.lower() in ['y', 'n']

        try:
            msg = await bot.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            embed = create_embed(ctx, 'Tic Tac Toe', description='Unable to start game, opponent did not respond in time.')
            await ctx.send(embed=embed)