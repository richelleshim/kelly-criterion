import os
import logging
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def calculate_kelly(win_prob: float, odds: float) :
    """
    Kelly formula: (p * (b + 1) - 1) / b
    where b = net decimal odds (odds - 1).
    """
    b = odds - 1
    k = (win_prob * (b + 1) - 1) / b
    return max(k, 0.0)

def convert_polymarket_to_odds(market_price: float) :
    """
    Decimal odds for YES = 1 / price.
    Decimal odds for NO  = 1 / (1 - price).
    ok so highkey this is no longer necessary bc i changed it but i'm kind of lazy to change it
    """
    return 1.0 / market_price

@bot.tree.command(
    name="kelly",
    description="Calculate Kelly Criterion for a Polymarket bet"
)
@app_commands.describe(
    your_fair_price="Your probability estimate of the event (0.0-1.0)",
    market_price="Current YES share price on Polymarket (0.0-1.0)",
)
async def slash_kelly(
    interaction: discord.Interaction,
    your_fair_price: float,
    market_price: float,
):
    odds = convert_polymarket_to_odds(market_price)
    effective_p = your_fair_price
    full_kelly = calculate_kelly(effective_p, odds)
    half_kelly = full_kelly / 2
    third_kelly = full_kelly / 3
    quarter_kelly = full_kelly / 4
    
    embed = discord.Embed(
        title="Polymarket Kelly Criterion Results",
        description=(
            f"Based on your **{your_fair_price*100:.1f}%** estimate and "
            f"**{market_price*100:.1f}%** market price"
        ),
        color=discord.Color.blue(),
    )
    embed.add_field(name="Implied Decimal Odds", value=f"{odds:.2f}", inline=False)
    embed.add_field(name="Full Kelly", value=f"{full_kelly:.2%} of bankroll", inline=False)
    embed.add_field(name="1/2 Kelly", value=f"{half_kelly:.2%} of bankroll", inline=False)
    embed.add_field(name="1/3 Kelly", value=f"{third_kelly:.2%} of bankroll", inline=False)
    embed.add_field(name="1/4 Kelly", value=f"{quarter_kelly:.2%} of bankroll", inline=False)
    if full_kelly == 0:
        embed.add_field(
            name="Notice",
            value="Kelly suggests **not** betting in this situation",
            inline=False,
        )
    embed.set_footer(text="🔢 Kelly = your edge vs. the market")
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="privatekelly",
    description="Calculate Kelly Criterion for a Polymarket bet (for your eyes only)"
)
@app_commands.describe(
    your_fair_price="Your probability estimate of the event (0.0-1.0)",
    market_price="Current YES share price on Polymarket (0.0-1.0)",
)
async def slash_privatekelly(
    interaction: discord.Interaction,
    your_fair_price: float,
    market_price: float,
):
    odds = convert_polymarket_to_odds(market_price, )
    effective_p = your_fair_price 
    full_kelly = calculate_kelly(effective_p, odds)
    half_kelly = full_kelly / 2
    third_kelly = full_kelly / 3
    quarter_kelly = full_kelly / 4
    
    embed = discord.Embed(
        title="Polymarket Kelly Criterion Results",
        description=(
            f"Based on your **{your_fair_price*100:.1f}%** estimate and "
            f"**{market_price*100:.1f}%** market price"
        ),
        color=discord.Color.blue(),
    )
    embed.add_field(name="Implied Decimal Odds", value=f"{odds:.2f}", inline=False)
    embed.add_field(name="Full Kelly", value=f"{full_kelly:.2%} of bankroll", inline=False)
    embed.add_field(name="1/2 Kelly", value=f"{half_kelly:.2%} of bankroll", inline=False)
    embed.add_field(name="1/3 Kelly", value=f"{third_kelly:.2%} of bankroll", inline=False)
    embed.add_field(name="1/4 Kelly", value=f"{quarter_kelly:.2%} of bankroll", inline=False)
    if full_kelly == 0:
        embed.add_field(
            name="Notice",
            value="Kelly suggests **not** betting in this situation",
            inline=False,
        )
    embed.set_footer(text="🔢 Kelly = your edge vs. the market")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(
    name="bankrollkelly",
    description="Calculate Kelly Criterion with exact amounts based on your bankroll (for your eyes only)"
)
@app_commands.describe(
    your_fair_price="Your probability estimate of the event (0.0-1.0)",
    market_price="Current YES share price on Polymarket (0.0-1.0)",
    bankroll="Your total bankroll amount (e.g. 1000)",
)
async def bankroll_kelly(
    interaction: discord.Interaction,
    your_fair_price: float,
    market_price: float,
    bankroll: float,
):
    # Input validation
    if not (0 < your_fair_price < 1):
        await interaction.response.send_message("Your fair price must be between 0 and 1", ephemeral=True)
        return
    
    if not (0 < market_price < 1):
        await interaction.response.send_message("Market price must be between 0 and 1", ephemeral=True)
        return
        
    if bankroll <= 0:
        await interaction.response.send_message("Bankroll must be positive", ephemeral=True)
        return
    
    odds = convert_polymarket_to_odds(market_price)
    effective_p = your_fair_price
    full_kelly = calculate_kelly(effective_p, odds)
    half_kelly = full_kelly / 2
    third_kelly = full_kelly / 3
    quarter_kelly = full_kelly / 4
    


    full_amount = full_kelly * bankroll
    half_amount = half_kelly * bankroll
    third_amount = third_kelly * bankroll
    quarter_amount = quarter_kelly * bankroll
    


    embed = discord.Embed(
        title="Bankroll-Based Kelly Criterion",
        description=(
            f"Based on your **{your_fair_price*100:.1f}%** estimate, "
            f"**{market_price*100:.1f}%** market price, and "
            f"**{bankroll:.2f}** bankroll"
        ),
        color=discord.Color.green(),
    )
    
    embed.add_field(name="Implied Decimal Odds", value=f"{odds:.2f}", inline=False)
    


    embed.add_field(
        name="Full Kelly", 
        value=f"{full_kelly:.2%} of your bankroll (${bankroll})= **${full_amount:.2f}**", 
        inline=False
    )
    embed.add_field(
        name="1/2 Kelly (Recommended)", 
        value=f"{half_kelly:.2%} of your bankroll (${bankroll})= **${half_amount:.2f}**", 
        inline=False
    )
    embed.add_field(
        name="1/3 Kelly (Recommended)", 
        value=f"{third_kelly:.2%} of your bankroll (${bankroll})= **${third_amount:.2f}**", 
        inline=False
    )
    embed.add_field(
        name="1/4 Kelly", 
        value=f"{quarter_kelly:.2%} of your bankroll (${bankroll})= **${quarter_amount:.2f}**", 
        inline=False
    )
    
    if full_kelly == 0:
        embed.add_field(
            name="Warning",
            value="Kelly suggests **not** betting in this situation",
            inline=False,
        )
    
    embed.set_footer(text="💰 Most professional bettors use half Kelly or less")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    print("Syncing commands globally (may take up to an hour to appear in all servers)")
    await bot.tree.sync() 
    print("Global command sync initiated")

bot.run(TOKEN)