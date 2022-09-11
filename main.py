import discord
from discord.ext import commands
import random
game = "hangman"
client = commands.Bot(command_prefix='/')

file = open('words.txt', 'r')
list_of_words = []
for line in file:
    list_of_words.append(line.strip())


@client.event
async def on_ready():
    print('ready')

@client.command()
async def online(ctx):
    await ctx.send("online")
    

#   --- hangman ---

async def update_keyword(keyword_hidden, keyword, msg):
    tmp_keyword_string = keyword_hidden
    for i in range(len(keyword)):
        if msg == keyword[i]:
            tmp_keyword_string[i] = keyword[i]
        else:
            tmp_keyword_string[i] = keyword_hidden[i]
    return ''.join(str(e) for e in tmp_keyword_string) + ' (' + str(len(keyword)) + ')'


async def update_graph(attempt):
    if attempt == 0:
        return '''> > gallows combs:
        >
        >
        >
        >
        >
        >
        > '''
    elif attempt == 1:
        return '''> > gallows combs:
        >
        >
        >
        >
        >
        >  /
        > '''
    elif attempt == 2:
        return '''> > gallows combs:
        >
        >
        >
        >
        >
        >  / \
        > '''
    elif attempt == 3:
        return '''> > gallows combs:
        >
        >     |
        >     |
        >     |
        >     |
        >  /_\
        > '''
    elif attempt == 4:
        return '''> >gallows combs:
        >       \_\_\_\_\_\_
        >     |
        >     |
        >     |
        >     |
        >  /_\
        > '''
    elif attempt == 5:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/
        >     |
        >     |
        >     |
        >  /_\
        > '''
    elif attempt == 6:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/           |
        >     |
        >     |
        >     |
        >  /_\
        > '''
    elif attempt == 7:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/           |
        >     |            O
        >     |
        >     |
        >  /_\
        > '''
    elif attempt == 8:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/           |
        >     |            O
        >     |             |
        >     |
        >  /_\
        > '''
    elif attempt == 9:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/           |
        >     |            O
        >     |           /|
        >     |
        >  /_\
        > '''
    elif attempt == 10:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/           |
        >     |            O
        >     |           /|\\
        >     |
        >  /_\
        > '''
    elif attempt == 11:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/           |
        >     |            O
        >     |           /|\\
        >     |           /
        >  /_\
        > '''
    elif attempt == 12:
        return '''> > gallows combs:
        >       \_\_\_\_\_\_
        >     |/           |
        >     |            O
        >     |           /|\\
        >     |           / \\
        >  /_\
        > '''


async def check_game_state(keyword_hidden, keyword, attempt):
    if attempt < 12 and keyword == keyword_hidden:
        print('1')
        return True, False
    elif attempt >= 12 and keyword != keyword_hidden:
        print('2')
        return False, True
    else:
        print('3')
        return False, False


def check(m):
    return len(m.content) == 1


async def hangmen(ctx):
    keyword_as_string = list_of_words[random.randint(0, len(list_of_words))].lower()
    keyword = list(keyword_as_string)
    keyword_hidden = []
    for i in range(len(keyword)):
        keyword_hidden.append('\_')
    attempt = 0
    used_letters = ['\n> ', 'Use letters: ']
    pic_str = await update_graph(attempt)
    keyword_string = ''.join(str(e) for e in keyword_hidden) + f' ({str(len(keyword))})'
    await ctx.send(f'''
                   > > Rules:
                   > - always just one letter, even if you already know the word
                   > no extra attempts are counted
                   > - lower case only
                   > - no numbers
                   > - instead of ö, ü, ä always ae, ue, oe\n {pic_str} {keyword_string}
    there are 58109  possible answers''')
    for i in range(len(keyword_as_string) + 12):
        win, lose = await check_game_state(keyword_hidden, keyword, attempt)
        print(keyword)
        if win:
            message = f'> GG, won with {str(attempt)} failed attempts!'
            break
        elif lose:
            message = f'> Nice try, unfortunately not good enough, the word was: {keyword_as_string}'
            await ctx.send(message)
            break
        else:
            msg = await client.wait_for('message', check=check)
            msg_str = msg.content.lower()
            if msg_str.isalpha():
                if msg_str in used_letters:
                    await ctx.send('>The letter has already been used.')
                else:
                    if msg_str not in keyword:
                        attempt += 1
                        pic_str = await update_graph(attempt)
                    elif msg_str in keyword:
                        pic_str = await update_graph(attempt)
                        keyword_string = await update_keyword(keyword_hidden, keyword, msg_str)
                    used_letters.append(msg_str)
                    used_letters_string = ''.join(str(e) for e in used_letters)
                    await ctx.send(pic_str + keyword_string + used_letters_string)
            else:
                await ctx.send('> There are no digits or special characters.')


#   --- commands ---

@client.command(pass_context=True, aliases=['gr', 'gallows combs'])
async def hangman(ctx):
    await hangmen(ctx)


#   --- events ---

@client.event
async def on_message(message):
    await client.process_commands(message)

client.run("OTMzODMyNDI3MTgzNDA3MTE0.GLJdin.KeYbwLLe2Ig2vpJ_wcGiA4CuRuMIw1764q5zgE")
