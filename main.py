import discord , json ,requests,os
from discord.ext import commands
from automessage import Automsg

os.system("pip install discord.py==1.7.3")

with open("config.json","r") as file:
 config = json.load(file)


upiid = config['upi']
TOKEN = config['token']
qri = config['qr']
vouch_id = config['vouch_id']
ltc = config['ltc']



intents = discord.Intents.default()


bot = commands.Bot(description='ASTA SELFBOT',
                           command_prefix='.',
                           self_bot=True,
                           intents=intents,help_command=None)



@bot.event
async def on_ready():
    print(f"{bot.user} Is Online")


def is_owner(ctx):
    return ctx.author.id == bot.user.id



@bot.command()
@commands.check(is_owner)
async def upi(ctx):
   await ctx.send(f"{upiid}")
   await ctx.send("**Please Send Screenshot After Payment**")


@bot.command()
@commands.check(is_owner)
async def qr(ctx):
   await ctx.send(f"{qri}")
   await ctx.send("**Please Send Screenshot After Payment**")

@bot.command()
@commands.check(is_owner)
async def i2c(ctx,amount:float):
   await ctx.send(f"`+rep <@{vouch_id}> LEGIT EXCHANGE •  [₹{amount}] UPI TO LTC")


@bot.command()
@commands.check(is_owner)
async def c2i(ctx,amount:float):
   await ctx.send(f"`+rep <@{vouch_id}> LEGIT EXCHANGE •  [${amount}] LTC TO UPI")


@bot.command()
@commands.check(is_owner)
async def addy(ctx):
   await ctx.send(f"{ltc}")
   await ctx.send("**Please Send Screenshot/Blockchain After Payment**")


@bot.command()
@commands.check(is_owner)
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltc}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("- `FAILED TO FETCH`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("`FAILED TO FETCH`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price

    message = f"**CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD`\n"
    message += f"**TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD`\n"
    message += f"**UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD`\n\n"

    await ctx.reply(message)

@bot.command()
@commands.check(is_owner)
async def bal(ctx,ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("- `FAILED`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("`FAILED TO FETCH`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price

    message = f"**LTC ADDRESS** : `{ltcaddress}`\n"
    message += f"**CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD`\n"
    message += f"**TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD`\n"
    message += f"**UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD`\n\n"

    await ctx.reply(message)


api_endpoint = 'https://api.mathjs.org/v4/'
@bot.command()
@commands.check(is_owner)
async def math(ctx, *, equation):
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.reply(f'`-` **RESULT**: `{result}`')
    else:
        await ctx.reply('`-` **FAILED**')


@bot.command()
@commands.check(is_owner)
async def delete(ctx, limit: int):
    """Deletes a specified number of your messages."""
    if limit <= 0:
        await ctx.reply("`-` Please specify a positive number of messages to delete.")
        return

    deleted = 0

    async for message in ctx.channel.history(limit=100):
        if message.author == ctx.author:
            try:
                await message.delete()
                deleted += 1
                if deleted == limit:
                    break
            except discord.Forbidden:
                await ctx.reply("`-` I don't have permission to delete messages.")
                return
            except discord.HTTPException:
                await ctx.reply("`-` Failed to delete messages due to an error.")
                return

    await ctx.reply(f"`+` Successfully deleted `{deleted}` of your messages.")




def setup(bot):
    bot.add_cog(Automsg(bot))
    bot.run(TOKEN,bot=False)


setup(bot)