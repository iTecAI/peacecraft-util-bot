import discord, time
from ipify import get_ip
from ip2geotools.databases.noncommercial import Freegeoip


client = discord.Client()
TOK = 'NDc2Njk0MTkyNzI3MjYxMTg1.DkxTyg.pVj32MDqiwS-rFWU6u0ZksEkEzo'
toggle = True

@client.event
async def on_ready():
    print('PCU Active')

@client.event
async def on_message(message):
    global toggle
    if message.channel.name == 'utilbots':
        if message.content.startswith('pcu ') or message.content.startswith('PCU '):
            cmd_help = {'test': 'Tests utilbot online status', 'help': 'Displays this information', 'server':'Displays relevant info about the MC server', 'ping':'Mentions everyone repeatedly. Specify this amount with a number after the ping command'} 
            cmd = message.content.split(' ')[1].lower()
            args = message.content.split(' ')[2:]
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
                loc_obj = Freegeoip.get(str(get_ip))
                loc = [loc_obj.latitude, loc_obj.longitude]
                await client.send_message(message.channel, 'LOC: ' + ', '.join(loc))
                
                    
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
            else:
                if toggle:
                    await client.send_message(message.channel, 'Error: invalid command.')
                

client.run(TOK)
