import discord
from discord.ext import commands
from discord import Intents, HTTPException
import asyncio
import random

token = ''
bot = commands.Bot(command_prefix='!', help_command=None, intents=Intents.all())




def WinnerGet(player1obj: str, player2obj: str):
    dados = {
        'rock': {
            'papel': 'perde', 'rock': 'empata', 'tesoura': 'ganha'
        },
        'papel': {
            'papel': 'empata', 'rock': 'ganha', 'tesoura': 'perde'
        },
        'tesoura': {
            'papel': 'ganha', 'rock': 'perde', 'tesoura': 'empata'
        }
    }
    if dados[player1obj][player2obj] == 'ganha':
         return 1
    elif dados[player1obj][player2obj] == 'empata':
        return 0
    else:
        return 2

def EmojiSelectGet(player1obj: str, player2obj: str):
    dados = {
        'rock': ':rock:',
        'papel': ':newspaper:',
        'tesoura': ':scissors:'
    }
    return dados[player1obj], dados[player2obj]


@bot.event
async def on_ready():
    sync = await bot.tree.sync()
    print(f'{len(sync)} Comandos Foram sincronizados.')
    print(f'Logado em {bot.user.name}')

jogando = []
select = {}
moves = ['rock', 'papel', 'tesoura']

class ResultEvent(discord.ui.View):
    def __init__(self, func):
        super().__init__()
        self.is_clicked = False
        self.Play = func
    @discord.ui.button(label='Jogar Novamente.', style=discord.ButtonStyle.blurple)
    async def JogarNovamente(self, inter: discord.Interaction, buttom: discord.ui.button):
        await self.Play(inter)


async def PlaySolo(inter: discord.Interaction):
    global jogando
    global select
    channel_url = f'https://discord.com/channels/{inter.channel.guild.id}/{inter.channel.id}'
    view = Menu(inter.user.id, channel_url)
    embed = discord.Embed(color=discord.Color.dark_blue(), title='Escolha uma das opcoes.')
    embed.add_field(inline=False, name='⬛ Pedra:', value='ganha de: Tesoura, perde para: Papel, empata com: Pedra')
    embed.add_field(inline=False, name='🧻 Papel:', value='ganha de: Pedra, perde para: Tesoura, empata com: Papel')
    embed.add_field(inline=False, name='✂ Tesoura:', value='ganha de: Papel, perde para: Pedra, empata com: Tesoura')
    message = await inter.response.send_message(embed=embed, view=view)
    timeout = 30
    count = 0
    n = False
    while not select.get(str(inter.user.id)):
        await asyncio.sleep(0.1)
        count += 0.1
        n = False
        if count == 20:
            n = True
            break
    if n:
        return
    player2obj = random.choice(moves)
    resultado = WinnerGet(select[str(inter.user.id)], player2obj)
    player1emoji, player2emoji = EmojiSelectGet(select[str(inter.user.id)], player2obj)
    view = ResultEvent(PlaySolo)
    if resultado == 1:
        await inter.edit_original_response(content='{} Ganhou!\n{}: {} vs {} :Bot'.format(inter.user.mention, inter.user.name, player1emoji, player2emoji), view=view, embed=None)
    elif resultado == 2:
        await inter.edit_original_response(content='Bot Ganhou!\n{}: {} vs {} :Bot'.format(inter.user.name, player1emoji, player2emoji), view=view, embed=None)
    else:
        await inter.edit_original_response(content='EMPATE! {}|Bot\n{}: {} vs {} :Bot'.format(inter.user.mention, inter.user.name, player1emoji, player2emoji), view=view, embed=None)
    del select[str(inter.user.id)]

class Menu(discord.ui.View):
    def __init__(self, id, channel_url = None):
        super().__init__()
        self.is_clicked = False
        self.id = id
        self.channel_url =  f'[Ir para o canal]({channel_url})'
    @discord.ui.button(label='Pedra', style=discord.ButtonStyle.gray, emoji='⬛')
    async def Pedrabutton(self, inter: discord.Interaction, button: discord.ui.Button):
        if not self.is_clicked:
            select[str(self.id)] = 'rock'
            await inter.response.send_message(f'Voce selecionou `Pedra`.\n{self.channel_url}', ephemeral=True)
            self.is_clicked = True
        else:
            await inter.response.send_message('Voce ja selecionou uma opçao.', ephemeral=True)
    @discord.ui.button(label='Papel', style=discord.ButtonStyle.green, emoji='🧻')
    async def Papelbutton(self, inter: discord.Interaction, button: discord.ui.Button):
        if not self.is_clicked:
            select[str(self.id)] = 'papel'
            await inter.response.send_message(f'Voce selecionou `Papel`.\n{self.channel_url}', ephemeral=True)
            self.is_clicked = True
        else:
            await inter.response.send_message('Voce ja selecionou uma opçao.', ephemeral=True)
    @discord.ui.button(label='Tesoura', style=discord.ButtonStyle.red, emoji='✂')
    async def TesouraButton(self, inter: discord.Interaction, button: discord.ui.Button):
        if not self.is_clicked:
            select[str(self.id)] = 'tesoura'
            await inter.response.send_message(f'Voce selecionou `Tesoura`.\n{self.channel_url}', ephemeral=True)
            self.is_clicked = True
        else:
            await inter.response.send_message('Voce ja selecionou uma opçao.', ephemeral=True)





@bot.tree.command(name='jokenpo', description='pedra papel tesoura.')
async def Jokenpo(inter: discord.Interaction, member: discord.Member= None):
    global jogando
    global select
    if member is not None and member:
        await inter.response.defer()
        jogadores = [inter.user, member]
        jogadores_id = [inter.user.id, member.id]
        for user in jogadores:
            jogando.append(int(user.id))
            channel_url = f'https://discord.com/channels/{inter.channel.guild.id}/{inter.channel.id}'
            view = Menu(user.id, channel_url)
            embed = discord.Embed(color=discord.Color.dark_blue(), description='Escolha uma das opcoes.')
            embed = discord.Embed(color=discord.Color.dark_blue(), title='Escolha uma das opcoes.')
            embed.add_field(inline=False, name='⬛ Pedra:', value='ganha de: Tesoura, perde para: Papel, empata com: Pedra')
            embed.add_field(inline=False, name='🧻 Papel:', value='ganha de: Pedra, perde para: Tesoura, empata com: Papel')
            embed.add_field(inline=False, name='✂ Tesoura:', value='ganha de: Papel, perde para: Pedra, empata com: Tesoura')
            await user.send(embed=embed, view=view)
        await inter.followup.send('Verifique suas dm.')
        timeout = 0
        n = False
        while not select.get('{}'.format(jogadores[0].id)) or not select.get('{}'.format(jogadores[1].id)):
            await asyncio.sleep(0.1)
            timeout += 0.1
            n = False
            if timeout == 20:
                n = True
                break
        if n:
            return None
        resultado = WinnerGet(select[str(jogadores[0].id)], select[str(jogadores[1].id)])
        player1emoji, player2emoji = EmojiSelectGet(select[str(jogadores[0].id)], select[str(jogadores[1].id)])
        if resultado == 1:
            await inter.followup.send('{} Ganhou!\n{}: {} vs {} :{}'.format(inter.user.mention, inter.user.name, player1emoji, player2emoji, member.name))
        elif resultado == 2:
            await inter.followup.send('{} Ganhou!\n{}: {} vs {} :{}'.format(member.mention, inter.user.name, player1emoji, player2emoji, member.name))
        else:
            await inter.followup.send('EMPATE! {} {}\n{}: {} vs {} :{}'.format(inter.user.mention, member.mention, inter.user.name, player1emoji, player2emoji, member.name))
        for jogador in jogadores_id:
            del select[str(jogador)]
    else:
        if member is None:
            await PlaySolo(inter)
        

try:
    bot.run(token)
except HTTPException as e:
    if e.status == 429:
        print('429: too many requests')