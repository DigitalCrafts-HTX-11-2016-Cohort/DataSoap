# coding=utf-8
import mysql.connector
connection = mysql.connector.connect(
    user='karissa',
    password='Vist@Pr0duction2017',
    host='35.166.251.127',
    database='dnc')

secret_key = 'szdfkg3vhojadz6dgad0rg'

# No longer using os specific commands. Keep below in case of future need
# os = "windows"
# os="linux"

# on dev, local = true. In deployment, set to false
local = True

if local:
    upload = "static/files_in/"
    download = "static/files_out/"
else:
    upload = "/var/www/FlaskApp/DNCApp/static/files_in/"
    download = "/var/www/FlaskApp/DNCApp/static/files_out/"
