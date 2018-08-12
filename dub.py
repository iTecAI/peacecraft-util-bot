import discord, time
from ipify import get_ip
from urllib.request import urlopen
import main_utils


client = discord.Client()
TOK = 'NDZ3MTZ1MTQ0OTgxMjAwODk2.Dk4XZg.Mvumy56qw1-NzR0F23y9sTNpFkU'
toggle = True
disabled_users = []
last = ''

@client.event
async def on_ready():
    print('PCU Active')

TOK = main_utils.RUC(TOK)
@client.event
async def on_message(message):
    global toggle, disabled_users, last
    if 'All we do is hack bots' in message.content:
        print('Located HAX')
        await client.delete_message(message)
        return
    if message.author in disabled_users:
        await client.delete_message(message)
        if last != message.author.name + ' tried to send a message but was disabled by an admin':
            await client.send_message(message.channel, message.author.name + ' tried to send a message but was disabled by an admin')
            last = message.author.name + ' tried to send a message but was disabled by an admin'
        return
    if message.channel.name == 'utilbots':
        if message.content.startswith('pcu ') or message.content.startswith('PCU '):
            cmd_help = {'test': 'Tests utilbot online status', 'help': 'Displays this information', 'server':'Displays relevant info about the MC server', 'ping':'Mentions everyone repeatedly. Specify this amount with a number after the ping command'} 
            cmd = message.content.split(' ')[1].lower()
            _args = message.content.split(' ')[2:]
            args = []
            c = 0
            while c < len(_args):
                if _args[c].startswith('['):
                    if _args[c].endswith(']'):
                        args.append(_args[c].strip('[]'))
                        c += 1
                    else:
                        print('COMPOUND')
                        arg = []
                        while not _args[c].endswith(']') and c < len(_args):
                            arg.append(_args[c].strip('['))
                            c += 1
                        arg.append(_args[c].strip(']'))
                        c += 1
                        args.append(' '.join(arg))
                else:
                    args.append(_args[c])
                    c += 1
                    
            print('RCV ' + cmd + ': ' + ', '.join(args))
            if cmd == 'test':
                await client.send_message(message.channel, 'System Online')
                await client.send_message(message.channel, 'Active: ' + str(toggle))
                await client.send_message(message.channel, 'Time: ' + time.ctime())
                mem_online = []
                for mem in message.server.members:
                    if mem.status != discord.Status.offline:
                        mem_online.append(str(mem.name) + ' (' + str(mem.nick) + ')')
                await client.send_message(message.channel, 'Online: ' + ', '.join(mem_online))
                raw = str(urlopen('https://api.ipgeolocation.io/ipgeo?apiKey=839e7eb39f7e4a958d348fdb9f87c47d&ip=' + str(get_ip())).read())
                raw = raw[2:len(raw)].strip(" '")
                loc = eval(raw, {'true':True, 'false': False})
                await client.send_message(message.channel, 'LOC: ' + ', '.join([loc['latitude'], loc['longitude']]))
                
                    
            elif cmd == 'server' and toggle:
                if len(args) >= 1:
                    if args[0] == 'ip':
                        await client.send_message(message.channel, 'Server IP: 207.38.165.56')
                    elif args[0] == 'owner':
                        await client.send_message(message.channel, 'Server Owner: Matteo | Discord: iTecX | Minecraft: MisitaLife')
                    else:
                        await client.send_message(message.channel, 'Error: Invalid argument ' + args[0])
                else:
                    await client.send_message(message.channel, 'Arguments/subcommands: \n-ip: Displays server IP \n-owner: gives info about server owner')
            elif cmd == 'help' and toggle:
                for i in cmd_help.keys():
                    await client.send_message(message.channel, i + ': ' + cmd_help[i])
            elif cmd == 'ping' and toggle:
                if len(args) == 0:
                    args[0] = 1
                try:
                    int(args[0])
                except:
                    args[0] = 1
                if message.author.name != 'iTecX' and int(args[0]) > 5:
                    await client.send_message(message.channel, 'Error: You cannot ping more than 5 times.')
                    return
                if len(args) == 1:
                    for i in range(abs(int(args[0]))):
                        if not toggle:
                            return
                        await client.send_message(message.channel, '@everyone')
                else:
                    to_men = None
                    for mem in message.server.members:
                        if mem.name == args[1] or mem.nick == args[1]:
                            to_men = mem.mention
                    if to_men == None:
                        await client.send_message(message.channel, 'Error: ' + args[1] + ' is not a member of this server')
                    else:
                        for i in range(abs(int(args[0]))):
                            if not toggle:
                                return
                            await client.send_message(message.channel, to_men)
            elif cmd == 'toggle' and message.author.name == 'iTecX':
                if toggle:
                    toggle = False
                else:
                    toggle = True
                await client.send_message(message.channel, '$PCU Active: ' + str(toggle))
            elif cmd == 'utoggle' and message.author.name == 'iTecX':
                try:
                    for i in message.mentions:
                        if i in disabled_users:
                            del disabled_users[disabled_users.index(i)]
                            await client.send_message(message.channel, 'Enabled ' + i.name)
                        else:
                            disabled_users.append(i)
                            await client.send_message(message.channel, 'Disabled ' + i.name)
                except:
                    pass
            else:
                if toggle:
                    await client.send_message(message.channel, 'Error: invalid command.')
                

client.run(TOK)
