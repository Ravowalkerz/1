import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

# Discord botunuzu oluşturun
bot = commands.Bot(command_prefix='!')
# Discord Components eklentisini başlatın
DiscordComponents(bot)

# Etkinlik bilgilerini tutacak bir sözlük oluşturun
events = {}

# Kullanıcı bilgilerini tutacak bir sözlük oluşturun
kullanici_bilgileri = {}

# Bot hazır olduğunda çalışacak fonksiyon
@bot.event
async def on_ready():
    print(f'{bot.user.name} botu olarak giriş yaptı!')

# "!etkinlik" komutunu tanımlayan fonksiyon
@bot.command(name='etkinlik')
async def etkinlik(ctx, *, etkinlik_adi):
    # Etkinlik adını ve ev sahibini sözlüğe ekleyin
    events[ctx.guild.id] = {'adi': etkinlik_adi, 'ev_sahibi': ctx.author.id}

    # Etkinlikle ilgili mesajı oluşturun
    etkinlik_mesaji = await ctx.send(f'{ctx.author.mention} tarafından "{etkinlik_adi}" etkinliği başlatıldı! Katılmak ister misiniz?',
                                      components=[Button(style=ButtonStyle.green, label="Evet"), Button(style=ButtonStyle.red, label="Hayır")])

    # Etkinlik mesajının ID'sini sözlüğe ekleyin
    events[ctx.guild.id]['mesaj_id'] = etkinlik_mesaji.id

# Buton tıklamalarını dinleyen fonksiyon
@bot.event
async def on_button_click(interaction):
    # Etkinlik mesajının ID'sini alın
    etkinlik_mesaj_id = events[interaction.guild.id]['mesaj_id']

    # Etkinlik mesajına yapılan bir buton tıklamasını kontrol edin
    if interaction.message.id == etkinlik_mesaj_id:
        # Ev sahibinin tıklamasını kontrol edin
        if interaction.user.id == events[interaction.guild.id]['ev_sahibi']:
            await interaction.respond(content="Etkinliğin ev sahibi olarak katılamazsınız!", ephemeral=True)
            return

        # Kullanıcının tıkladığı butonun değerine göre işlem yapın
        if interaction.component.label == "Evet":
            await interaction.respond(content=f"{interaction.user.mention} katılımınız onaylandı!", ephemeral=True)
        elif interaction.component.label == "Hayır":
            await interaction.respond(content=f"{interaction.user.mention} katılımınız reddedildi!", ephemeral=True)

# "!bilgi" komutunu tanımlayan fonksiyon
@bot.command(name='bilgi')
async def bilgi(ctx, *, args):
    # Kullanıcının adını ve bilgilerini ayırın
    kullanici_adı, *bilgiler = args.split()

    # Kullanıcı adı zaten kayıtlı mı kontrol edin
    if kullanici_adı in kullanici_bilgileri:
        await ctx.send(f"{kullanici_adı} adlı kullanıcı zaten kayıtlı. Bilgileri güncellemek için '!guncelle' komutunu kullanabilirsiniz.")
    else:
        # Kullanıcı adını ve bilgileri sözlüğe ekleyin
        kullanici_bilgileri[kullanici_adı] = {
            'ap': None,
            'aap': None,
            'dp': None,
            'class': None,
            'trina_baltasi': None
        }

        for bilgi in bilgiler:
            anahtar, deger = bilgi.split(':')
            if anahtar.lower() in kullanici_bilgileri[kullanici_adı]:
                kullanici_bilgileri[kullanici_adı][anahtar.lower()] = deger

        await ctx.send(f"{kullanici_adı} adlı kullanıcının bilgileri başarıyla kaydedildi.")

# "!guncelle" komutunu tanımlayan fonksiyon
@bot.command(name='guncelle')
async def guncelle(ctx, *, args):
    # Kullanıcının adını ve bilgilerini ayırın
    kullanici_adı, *guncel_bilgiler = args.split()

    # Kullanıcı adı kayıtlı mı kontrol edin
    if kullanici_adı not in kullanici_bilgileri:
        await ctx.send(f"{kullanici_adı} adlı kullanıcı kayıtlı değil. Bilgi eklemek için '!bilgi' komutunu kullanabilirsiniz.")
    else:
        for bilgi in guncel_bilgiler:
            anahtar, deger = bilgi.split(':')
            if anahtar.lower() in kullanici_bilgileri[kullanici_adı]:
                kullanici_bilgileri[kullanici_adı][anahtar.lower()] = deger

        await ctx.send(f"{kullanici_adı} adlı kullanıcının bilgileri başarıyla güncellendi.")

# "!gs" komutunu tanımlayan fonksiyon
@bot.command(name='gs')
async def gs(ctx):
    # Kullanıcı bilgilerini listeleyin
    for i, (kullanici, bilgiler) in enumerate(kullanici_bilgileri.items(), start=1):
        bilgi_str = f"{i}. Nick:{kullanici} ap:{bilgiler['ap']} aap:{bilgiler['aap']} dp:{bilgiler['dp']} class:{bilgiler['class']} trina baltası:{bilgiler['trina_baltasi']}"
        await ctx.send(bilgi_str)

# Botu çalıştırın
bot.run(MTE3ODgwNzAzMzA1NTY3ODU2Ng.G4YGnD.5JYcqIyfiBPNkuvkjVaY5IXsD3BSOBTPk5_S3w)
