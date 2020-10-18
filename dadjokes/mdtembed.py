import discord
# import requests
from validator_collection import validators


class Embed:
    def __init__(self, bot):
        self.bot = bot

    def create(self, ctx, color=discord.Color.gold(), title='', description='', image=None,
               thumbnail=None, url=None, footer_text=None, footer_url=None, author_text=None):
        '''Return a color styled embed with MDT footer, and optional title or description.
        user_id = user id string. If none provided, takes message author.
        color = manual override, otherwise takes gold for private channels, or author color for guild.
        title = String, sets title.
        description = String, sets description.
        image = String url.  Validator checks for valid url.
        thumbnail = String url. Validator checks for valid url.'''
        DEMARATUS_ICON = 'https://cdn.discordapp.com/attachments/745608075670585344/767361428910637066/demaratuscircle.png'
        PATREON = 'https://patreon.com/matrixdt'
        MDT_LOGO = 'https://cdn.discordapp.com/attachments/745608075670585344/767361113477611580/MatrixDevelopmentTeam.png'

        if isinstance(ctx.message.channel, discord.abc.GuildChannel):
            color = ctx.message.author.color
        if url is None:
            url = PATREON
        data = discord.Embed(color=color, title=title, url=url)
        if description is not None:
            if len(description) < 1500:
                data.description = description
        data.set_author(name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.avatar_url)
        if image is not None:
            validators.url(image)
            code = requests.get(image).status_code
            if code == 200:
                data.set_image(url=image)
            else:
                print('Image URL Failure, code {}'.format(code))
                print('Attempted URL:\n{}'.format(image))
        if thumbnail is None:
            thumbnail = DEMARATUS_ICON
        if thumbnail is not None:
            validators.url(thumbnail)
            code = requests.get(thumbnail).status_code
            if code == 200:
                # data.set_thumbnail(url=thumbnail)
                data.set_thumbnail(
                    url=thumbnail)
            else:
                data.set_thumbnail(url=DEMARATUS_ICON)
                print('Thumbnail URL Failure, code {}'.format(code))
                print('Attempted URL:\n{}'.format(thumbnail))
        if footer_text is None:
            footer_text = "Demaratus | Matrix Development Team"
        if footer_url is None:
            footer_url = DEMARATUS_ICON
        data.set_footer(text=footer_text, icon_url=footer_url)
        return data
