import asyncio
import discord
import json
import random
from datetime import datetime
from discord.ext import commands
import os
import classschedule

# https://discord.com/api/oauth2/authorize?client_id=796805491186597968&permissions=2147483639&scope=bot

# with open('config.json', 'r') as f:
#     token_dict = json.load(f)
#     BOT_TOKEN = token_dict['token']

PREFIX = '$'

bot = commands.Bot(command_prefix=PREFIX, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'{PREFIX}help | this is a good bot'))

@bot.event
async def on_message(message):
    if message.author.id != 796805491186597968:
        if random.randint(1,200) == 1:
            await message.add_reaction('🍾')
            sent = await message.channel.send(f'{message.author.mention} lol get bottled')
            print(f'{message.author} was bottled!')
    await bot.process_commands(message)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            author1 = await ctx.guild.fetch_member(688530998920871969)
            embed = create_embed(ctx, 'Bot Commands', description=f'Written by {author1.mention}.')
            embed.add_field(name='Fun Commands', value=f'`{PREFIX}help fun`', inline=False)
            embed.add_field(name='School Commands', value=f'`{PREFIX}help school`', inline=False)
            embed.add_field(name='Informational Commands', value=f'`{PREFIX}help info`', inline=False)
            embed.add_field(name='Server Moderation Commands', value=f'`{PREFIX}help mod`', inline=False)
            embed.add_field(name='Link Commands', value=f'`{PREFIX}help link`', inline=False)
            await ctx.send(embed=embed)
            log_command(ctx)

    @help.command(name='fun')
    async def _fun(self, ctx):
        embed = create_embed(ctx, 'Fun Commands')
        embed.add_field(name=f'{PREFIX}hello', value='Allows you to greet the bot and earn some coins.', inline=False)
        embed.add_field(name=f'{PREFIX}8ball <question>', value='Ask a question, get an answer.', inline=False)
        embed.add_field(name=f'{PREFIX}rng <minimum> <maximum>', value='Generate a random number between two numbers.', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='info')
    async def _info(self, ctx):
        embed = create_embed(ctx, 'Informational Commands')
        embed.add_field(name=f'{PREFIX}ping', value='Tells you the latency of the bot (basically my WiFi speed lol).', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='mod')
    async def _mod(self, ctx):
        embed = create_embed(ctx, 'Server Moderation Commands')
        embed.add_field(name=f'{PREFIX}purge <message count>', value='Purges messages from the current channel.', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

    @help.command(name='link')
    async def _link(self, ctx):
        embed = create_embed(ctx, 'Link Commands')
        embed.add_field(name=f'{PREFIX}safety', value='Links to Safety Dance.', inline=False)
        embed.add_field(name=f'{PREFIX}tainted', value='Links to Tainted Love.', inline=False)
        embed.add_field(name=f'{PREFIX}goldenhair', value='Links to Sister Golden Hair.', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @help.command(name='school')
    async def _info(self, ctx):
        embed = create_embed(ctx, 'School Commands')
        embed.add_field(name=f'{PREFIX}register <blue day lunch> <gold day lunch> <cohort>', value=f'Example: `{PREFIX}register B D greyhound`\nAllows you to register details with the bot to get personalized responses.\nAll three values are required.\nOther commands will currently not work without registration.', inline=False)
        embed.add_field(name=f'{PREFIX}currentday [all]', value='Tells you information about today (Blue/Gold, In Person/Virtual, Late Start, weekends, breaks, etc.).\nThe `all` argument is optional, and it will display information for both cohorts.', inline=False)
        embed.add_field(name=f'{PREFIX}currentweek [all]', value='Tells you information about the next seven days.\nThe `all` argument is optional, and it will display information for both cohorts.', inline=False)
        embed.add_field(name=f'{PREFIX}date <date> [all]', value='Tells you information about a specified date.\nThe `date` argument is required, and must be in the form `mm/dd/yyyy`.\nThe `all` argument is optional, and it will display information for both cohorts.', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

bot.add_cog(Help(bot))

class School(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _register(self, user_id, blue_lunch, gold_lunch, cohort):
        user_id = str(user_id)
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        if user_id not in school_dict:
            with open('school.json', 'w') as f:
                school_dict[user_id] = {}
                school_dict[user_id]['blue_lunch'] = blue_lunch
                school_dict[user_id]['gold_lunch'] = gold_lunch
                school_dict[user_id]['cohort'] = cohort,
                json.dump(school_dict, f)

    def _register_class(self, user_id, class_id, class_name):
        class_id = str(class_id)
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        if user_id not in school_dict:
            with open('school.json', 'w') as f:
                if not school_dict[user_id]['classes']:
                    school_dict[user_id]['classes'] = {}
                school_dict[user_id]['classes'][class_id] = class_name
                json.dump(school_dict, f)

    def _registration_checks(self, ctx):
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        return str(ctx.author.id) in school_dict

    def _class_registration_checks(self, ctx, class_id):
        with open('school.json', 'r') as f:
            school_dict = json.load(f)
        return str(ctx.author.id) in school_dict
    
    def _get_users_dict(self):
        with open('school.json', 'r') as f: 
            school_dict = json.load(f)
        return school_dict

    def _get_user_info(self, user: str):
        with open('school.json', 'r') as f: 
            school_dict = json.load(f)
        return school_dict[user]
    
    def _set_users_dict(self, school_dict):
        with open('school.json', 'w') as f:
            json.dump(school_dict, f)
    
    @commands.command()
    async def register(self, ctx, blue_lunch, gold_lunch, cohort):
        self._register(ctx.author.id, blue_lunch, gold_lunch, cohort)
        desc = f'You have been registered.'
        embed = create_embed(ctx, 'User Registration', description=desc)
        embed.add_field(name='Blue Day Lunch', value=blue_lunch, inline=False)
        embed.add_field(name='Gold Day Lunch', value=gold_lunch, inline=False)
        embed.add_field(name='Cohort', value=cohort, inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.command(name='registerclass')
    async def register_class(self, ctx, class_id, class_name):
        self._register_class(ctx.author.id, class_id.lower(), class_name)
        desc = f'{ctx.author.mention}, you have been registered.'
        embed = create_embed(ctx, 'Class Registration', description=desc)
        embed.add_field(name=class_id, value=class_name, inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.group()
    async def currentday(self, ctx, arg=None):
        if ctx.invoked_subcommand is None:
            if not self._registration_checks(ctx):
                embed = create_embed(ctx, 'Error', description="You must be registered to use this command. Try appending `all` to the command, or registering.")
                await ctx.send(embed=embed)
                return
            user_info = self._get_user_info(str(ctx.author.id))
            school_day = classschedule.get_current_day(user_info)
            desc = f'Today is {datetime.now().strftime("%A, %B %d, %Y")}.\nYour Cohort ({user_info["cohort"].title()}): {school_day}'
            embed = create_embed(ctx, 'School Day', desc)
            await ctx.send(embed=embed)
            log_command(ctx)
    
    @currentday.command(name='all')
    async def currentday_all(self, ctx):
        school_day = classschedule.get_current_day()
        desc = f'Today is {datetime.now().strftime("%A, %B %d, %Y")}.\nCarmel Cohort: {school_day[0]}.\nGreyhound Cohort: {school_day[1]}.\n'
        embed = create_embed(ctx, 'School Day', desc)
        await ctx.send(embed=embed)
        log_command(ctx)

    @commands.group()
    async def currentweek(self, ctx):
        if ctx.invoked_subcommand is None:
            if not self._registration_checks(ctx):
                embed = create_embed(ctx, 'Error', description="You must be registered to use this command. Try appending `all` to the command, or registering.")
                await ctx.send(embed=embed)
                return
            user_info = self._get_user_info(str(ctx.author.id))
            school_week = classschedule.get_week(user_info)
            desc = '\n'.join(school_week)
            embed = create_embed(ctx, 'School Week', desc)
            await ctx.send(embed=embed)
            log_command(ctx)
    
    @currentweek.command(name='all')
    async def currentweek_all(self, ctx):
        school_weeks = classschedule.get_week()
        embed = create_embed(ctx, 'School Week')
        value1='\n'.join(school_weeks[0])
        embed.add_field(name='Carmel Cohort', value=value1)
        value2='\n'.join(school_weeks[1])
        embed.add_field(name='Greyhound Cohort', value=value2)
        await ctx.send(embed=embed)
        log_command(ctx)
    
    @commands.group()
    async def date(self, ctx, date):
        if ctx.invoked_subcommand is None:
            if not self._registration_checks(ctx):
                embed = create_embed(ctx, 'Error', description="You must be registered to use this command. Try appending `all` to the command, or registering.")
                await ctx.send(embed=embed)
                return
            user_info = self._get_user_info(str(ctx.author.id))
            school_day = classschedule.get_day(date, user_info)
            desc = f'Your Cohort ({user_info["cohort"].title()}): {school_day}'
            embed = create_embed(ctx, 'School Day', desc)
            await ctx.send(embed=embed)
            log_command(ctx)
    
    @date.command(name='all')
    async def date_all(self, ctx, date):
        school_day = classschedule.get_day(date)
        desc = f'Carmel Cohort: {school_day[0]}\nGreyhound Cohort: {school_day[1]}\n'
        embed = create_embed(ctx, 'School Day', desc)
        await ctx.send(embed=embed)
        log_command(ctx)

bot.add_cog(School(bot)) 

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _registration_checks(self, ctx):
        with open('currency.json', 'r') as f:
            currency = json.load(f)
        if str(ctx.author.id) not in currency:
            with open('currency.json', 'w') as f:
                currency[str(ctx.author.id)] = 0
                json.dump(currency, f)
    
    def _get_currency_dict(self, ctx):
        self._registration_checks(ctx)
        with open('currency.json', 'r') as f:
            currency = json.load(f)
        return currency
    
    def _set_currency_dict(self, ctx, currency):
        self._registration_checks(ctx)
        with open('currency.json', 'w') as f:
            json.dump(currency, f)

    def increment_coins(self, ctx, coins: int):
        currency = self._get_currency_dict(ctx)
        currency[str(ctx.author.id)] += coins
        self._set_currency_dict(ctx, currency)
    
    async def command_coins(self, ctx, max_coin_count: int=5):
        if random.randint(0,100) >= 80:
            coin_count = random.randint(2, max_coin_count)
            self.increment_coins(ctx, coin_count)
            color = discord.Color.green()
            embed = discord.Embed(title='Coins!', description=f'Nice! You got {coin_count} coins!', color=color)
            await ctx.send(embed=embed)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        bal = self._get_currency_dict(ctx)
        embed = create_embed(ctx, 'Balance', f'You have {bal[str(ctx.author.id)]} coins.')
        await ctx.send(embed=embed)
        log_command(ctx)
    
bot.add_cog(Economy(bot))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        embed = create_embed(ctx, 'Hello!', description=f'How are you, {ctx.author.mention}?')
        await ctx.send(embed=embed)
        await bot.get_cog('Economy').command_coins(ctx)
        log_command(ctx)
    
    @commands.command(name='8ball')
    async def eightball(self, ctx, arg):
        responses = [
            [
                ':green_circle: As I see it, yes. :green_circle:',
                ':green_circle: It is certain. :green_circle:',
                ':green_circle: It is decidedly so. :green_circle:',
                ':green_circle: Most likely. :green_circle:',
                ':green_circle: Outlook good. :green_circle:',
                ':green_circle: Signs point to yes. :green_circle:',
                ':green_circle: Without a doubt. :green_circle:',
                ':green_circle: Yes. :green_circle:',
                ':green_circle: Yes, definitely. :green_circle:',
                ':green_circle: You may rely on it. :green_circle:'
            ],
            [
                ':red_circle: Very doubtful. :red_circle:',
                ':red_circle: My reply is no. :red_circle:',
                ':red_circle: My sources say no. :red_circle:',
                ':red_circle: Outlook not so good. :red_circle:',
                ':red_circle: Don’t count on it. :red_circle:',
            ],
            [
                ':yellow_circle: Ask again later. :yellow_circle:',
                ':yellow_circle: Better not tell you now. :yellow_circle:',
                ':yellow_circle: Cannot predict now. :yellow_circle:',
                ':yellow_circle: Concentrate and ask again. :yellow_circle:',
                ':yellow_circle: Reply hazy, try again. :yellow_circle:',
            ],
        ]
        response_category = responses[random.randint(0,2)]
        desc = response_category[random.randint(0, len(response_category)-1)]
        embed = create_embed(ctx, 'Magic 8 Ball', description=desc)
        await ctx.send(embed=embed)
        await bot.get_cog('Economy').command_coins(ctx)
        log_command(ctx)
    
    @commands.command()
    async def rng(self, ctx, minnum:int, maxnum: int):
        await ctx.send(random.randint(minnum, maxnum))
        await bot.get_cog('Economy').command_coins(ctx)
        log_command(ctx)

bot.add_cog(Fun(bot))

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

bot.add_cog(Games(bot))

class Links(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def safety(self, ctx):
        embed = create_embed(ctx, 'Safety Dance', url='https://www.youtube.com/watch?v=AjPau5QYtYs')
        await ctx.send(embed=embed)
        await bot.get_cog('Economy').command_coins(ctx)
        log_command(ctx)

    @commands.command()
    async def tainted(self, ctx):
        embed = create_embed(ctx, 'Tainted Love', url='https://www.youtube.com/watch?v=ZcyCQLewj10')
        await ctx.send(embed=embed)
        await bot.get_cog('Economy').command_coins(ctx)
        log_command(ctx)

    @commands.command()
    async def goldenhair(self, ctx):
        embed = create_embed(ctx, 'Sister Golden Hair', url='https://www.youtube.com/watch?v=XIycEe59Auc')
        await ctx.send(embed=embed)
        await bot.get_cog('Economy').command_coins(ctx)
        log_command(ctx)

bot.add_cog(Links(bot))

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = create_embed(ctx, 'Pong!', description=f'`{round(bot.latency * 1000, 1)}ms`')
        await ctx.send(embed=embed)
        log_command(ctx)

    @commands.command()
    async def version(self, ctx):
        embed = create_embed(ctx, 'Version History')
        embed.add_field(name='Current Version', value='`0.0.1`', inline=False)
        await ctx.send(embed=embed)
        log_command(ctx)

bot.add_cog(Info(bot))

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, num: int):
        if ctx.author.guild_permissions.manage_messages == True:
            msgs = []
            async for x in ctx.channel.history(limit=num):
                msgs.append(x)
            await ctx.channel.delete_messages(msgs)
            embed = create_embed(ctx, 'Message Purge', f'{num} messages deleted.')
            await ctx.send(embed=embed)
            asyncio.sleep(5)
        else:
            embed = create_embed(ctx, 'Message Purge', 'You do not have the required permission to run this command (Manage Messages).')
            await ctx.send(embed=embed)
    
    @commands.command()
    async def purge(self, ctx, num: int):
        if ctx.author.guild_permissions.manage_messages == True:
            msgs = []
            async for x in ctx.channel.history(limit=num):
                msgs.append(x)
            await ctx.channel.delete_messages(msgs)
            embed = create_embed(ctx, 'Message Purge', f'{num} messages deleted.')
            await ctx.send(embed=embed)
        else:
            embed = create_embed(ctx, 'Message Purge', 'You do not have the required permission to run this command (Manage Messages).')
            await ctx.send(embed=embed)
    
    @commands.command()
    async def kick(self, ctx, user: discord.User, reason: str=None):
        if ctx.author.guild_permissions.kick_members == True:
            await ctx.guild.kick(user, reason=reason)
            desc = f'{user} has been kicked.'
            if reason:
                desc += f'\nReason: {reason}'
            embed = create_embed(ctx, 'User Kick', description=desc)
            await ctx.send(embed=embed)
        else:
            embed = create_embed(ctx, 'User Kick', 'You do not have the required permission to run this command (Ban Members).')
            await ctx.send(embed=embed)
        
    @commands.command()
    async def ban(self, ctx, user: discord.User, reason: str=None):
        if ctx.author.guild_permissions.ban_members == True:
            await ctx.guild.ban(user, reason=reason)
            desc = f'{user} has been banned.'
            if reason:
                desc += f'\nReason: {reason}'
            embed = create_embed(ctx, 'User Ban', description=desc)
            await ctx.send(embed=embed)
        else:
            embed = create_embed(ctx, 'User Ban', 'You do not have the required permission to run this command (Ban Members).')
            await ctx.send(embed=embed)

bot.add_cog(Moderation(bot))

@bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

def create_embed(ctx, title, description=None, url=None):
    embed = discord.Embed(title=title, description=description, url=url)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f'Server: {ctx.guild} | Command: {ctx.message.content}', icon_url=ctx.guild.icon_url)
    return embed

def log_command(ctx):
    print(f'{ctx.author} ran {ctx.message.content}.')

bot.run(os.environ['token']) # bot token