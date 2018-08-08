import discord
import time

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
            _args = message.content.split(' ')[2:]
            args = []
            for i in _args:
                args.append(i.lower())
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
                if message.author.name != 'iTecX' and int(args[0]) > 5:
                    await client.send_message(message.channel, 'Error: You cannot ping more than 5 times.')
                    return
                for i in range(abs(int(args[0]))):
                    if not toggle:
                        return
                    await client.send_message(message.channel, '@everyone')
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
