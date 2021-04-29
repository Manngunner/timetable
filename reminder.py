"""
Copyright (C) 2021  Berat Gökgöz

This file is a part of Timetable project.

Timetable is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any
later version.

Timetable is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord
import re

hugeregex = r'(((([012]\d)|(\d)|(30))[/.-](([0][469])|([1][1])))|((([012]\d)|(\d)|(3[01]))[/.-](([0][13578])|([1][02])))|((([01]\d)|(\d)|([2][012345678]))[/.-]((02)|(2))))[/.-]((20[2][123456789])|(20[3456789]\d))'
timeregex = r'(([01][0123456789])|(\d)|([2][0123]))[:.]([012345]\d)'

async def reminder(ctx, cmd, args, bot, db, getDate, getDayTime, get_prefix):
    if cmd=='' or cmd == None:
        await ctx.channel.send(embed=discord.Embed(
        description=f"Subcommands add/create:\n\
Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn.\n\
\nSubcommands remove/delete:\n\
Usage: {get_prefix(None, ctx)}reminder remove/delete ID\n\
Note: There is no difference between delete and remove or add and create subcommands.", colour=0xACB6C4))
        return
    cmand = cmd.lower().strip()
    params = ' '.join(args)
    if cmand == "create" or cmand == "add":
        try:
            channelId = re.search(r'(\d){18}', args[2]).group().strip('<').strip('>').strip('#')
            if channelId is None:
                await ctx.channel.send(embed=discord.Embed(
                    description=f"Usage: {get_prefix(None, ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn.",
                    colour=0xACB6C4))
                return
        except AttributeError:
            await ctx.channel.send(embed=discord.Embed(
            description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn.", colour=0xACB6C4))
            return
        if "today" in params:
            reminderDate = getDate()
        elif "tomorrow" in params:
            reminderDate = getDate("tomorrow")
        else:
            result = None
            try:
                result = re.search(hugeregex, params).group()
            except AttributeError:
                await ctx.channel.send(embed=discord.Embed(
                description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn.", colour=0xACB6C4))
                return
            if result != None:
                result = result.replace('/', '-').replace('.', '-').split('-')
                result[0] = result[0].lstrip('0')
                result[1] = result[1].lstrip('0')
                reminderDate = '-'.join(result)
            elif result == None:
                await ctx.channel.send(embed=discord.Embed(
                description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn.", colour=0xACB6C4))
                return
        searchTime = None
        searchTime = re.search(timeregex, params).group()
        if searchTime == None:
            await ctx.channel.send(embed=discord.Embed(
            description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn.", colour=0xACB6C4))
            return
        elif searchTime != None:
            reminderTime = searchTime.replace(':', '_').replace('.', '_')
        remId = db.addReminder(reminderDate, reminderTime, channelId, ' '.join(params.split()[3:]))
        await ctx.channel.send(f"Reminder {' '.join(params.split()[3:])} with ID {remId} has successfully set to {reminderDate.replace('-', '/')} {reminderTime.replace('_',':')}.\nIt will be announced at channel <#{channelId}>")

    elif cmand == "delete" or cmand == "remove":
        if len(params.split())==1:
            remId = re.search(r'([1-9])([0-9]{5})')
            db.delReminder(remId)
        else:
            await ctx.channel.send(f'Usage: {get_prefix(None, ctx)}reminder remove/delete ID')
    else:
        await ctx.channel.send("There isn't a reminder command like that.")
        return
