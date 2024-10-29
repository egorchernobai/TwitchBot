import time
from twitchio.ext import commands, routines
import random
import configparser, codecs


config = configparser.ConfigParser()
config.read_file(codecs.open("config.ini", "r", "utf-8"))
TOKEN = config["BOT"]["TOKEN"]
CHAT = config["BOT"]["CHAT"].split()
PERFIX = config['BOT']["PERFIX"]
HP = int(config['BOT']["HP"])
HIT = int(config['BOT']["HIT"])
MESS_START = config['BOT']["MESS_START"].split(", ")
MESS_END = config['BOT']["MESS_END"].split(", ")
MESS_HIT = config['BOT']["MESS_HIT"].split(", ")
MESS_BOT_IS_DEAD = config['BOT']["MESS_BOT_IS_DEAD"].split(", ")
LISTOP = config['BOT']["LISTOP"].split(", ")
USER_TIMEOUT = int(config['BOT']["USER_TIMEOUT"])
BOT_TIMEOUT = int(config['BOT']["BOT_TIMEOUT"])
MESS_TIMEOUT = int(config['BOT']["MESS_TIMEOUT"])
MESS_NAPOM = config['BOT']["MESS_NAPOM"].split(", ")


class Bot(commands.Bot):
	def __init__(self):
		super().__init__(token=TOKEN, prefix=PERFIX, initial_channels=CHAT)

	async def event_ready(self):
		print(f'Logged in as | {self.nick}')


	@commands.command()
	async def hit(self, ctx: commands.Context):
		if self.hp - self.hit > 0 and ((ctx.author.name not in self.users) or self.users.get(ctx.author.name) + USER_TIMEOUT <= time.time()):
			self.hp -= self.hit
			await ctx.send(random.choice(MESS_HIT))
			if ctx.author.name in self.users_uron:
				self.users_uron[ctx.author.name] += self.hit
			else:
				 self.users_uron[ctx.author.name] = self.hit
			self.users[ctx.author.name] = time.time()
			self.tme = time.time()
		elif self.hp - self.hit <= 0 and ((ctx.author.name not in self.users) or self.users.get(ctx.author.name) + USER_TIMEOUT <= time.time()):
			await ctx.send(random.choice(MESS_END))
			if ctx.author.name in self.users_uron:
				self.users_uron[ctx.author.name] += self.hp
			else:
				self.users_uron[ctx.author.name] = self.hp
			self.hp -= HP
			sorted_keys = sorted(self.users_uron, key=self.users_uron.get)
			sorted_user_uron = dict()
			for w in sorted_keys:
				sorted_user_uron[w] = self.users_uron[w]
			if len(sorted_user_uron) >= 3:
				await ctx.send(f'**Топ по урону**\n Топ-1: {sorted_keys[-1]}, он нанес {sorted_user_uron[sorted_keys[-1]]} урона,\n Топ-2: {sorted_keys[-2]}, он нанес {sorted_user_uron[sorted_keys[-2]]}урона,\n Топ-3: {sorted_keys[-3]}, он нанес {sorted_user_uron[sorted_keys[-3]]} урона\n')
			elif len(sorted_user_uron) == 2:
				await ctx.send(f'**Топ по урону**\n Топ-1: {sorted_keys[-1]}, он нанес {sorted_user_uron[sorted_keys[-1]]} урона,\n Топ-2: {sorted_keys[-2]}, он нанес {sorted_user_uron[sorted_keys[-2]]}урона.')
			else:
				await ctx.send(f'**Топ по урону**\n Топ-1: {sorted_keys[-1]}, он нанес {sorted_user_uron[sorted_keys[-1]]} урона.')
			self.bot_stop_time = time.time()
			self.hp = 0
			self.tme = time.time()
			bot.bot_start_automatic.start(ctx)

		elif ctx.author.name in self.users and self.users.get(ctx.author.name) + USER_TIMEOUT > time.time():
			self.tme = time.time()
			await ctx.send(f"**{ctx.author.name}, вам нельзя атаковать бота еще {str(self.users[ctx.author.name] - time.time() + USER_TIMEOUT)[0:2]} секунд**")
		elif self.hp < 0:
			await ctx.send(random.choice(MESS_BOT_IS_DEAD))

	@commands.command()
	async def start(self, ctx: commands.Context):
		if ctx.author.name in LISTOP:
			await ctx.send(random.choice(MESS_START))
			self.hp = HP
			self.hit = HIT
			self.users = dict()
			self.users_uron = dict()
			self.tme = time.time()
			bot.bot_napom.start(ctx)
	
	@commands.command()
	async def hp(self, ctx: commands.Context):
		if self.hp > 0:
			await ctx.send(f'**осталось {self.hp} хп**')
		else:
			await ctx.send(random.choice(MESS_BOT_IS_DEAD))


	@routines.routine(seconds=int(BOT_TIMEOUT))
	async def bot_start_automatic(self, ctx):
		if self.hp == 0 and int(self.bot_stop_time) + int(BOT_TIMEOUT) < int(time.time()):
			self.hp = HP
			self.hit = HIT
			self.users = dict()
			self.users_uron = dict()
			await ctx.send(random.choice(MESS_START))

	@routines.routine(seconds=MESS_TIMEOUT)
	async def bot_napom(self, ctx):
		if self.hp != 0 and self.tme + USER_TIMEOUT + MESS_TIMEOUT < time.time():
			await ctx.send(random.choice(MESS_NAPOM))




bot = Bot()
bot.run()
