import os


class Constants:
    prefix = ','
    discord_token = os.environ.get('discord', None)  # dev
    osu_api_key = os.environ.get('osu', None)
    support_server_link = 'https://invite.gg/cspound'
    version = '2.2'
    invite_link = 'https://www.tailstar.us/'
    mongodb_connection_string = os.environ.get('mongodb', None)
