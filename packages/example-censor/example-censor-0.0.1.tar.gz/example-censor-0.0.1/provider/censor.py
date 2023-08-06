from provider.profanity_provider import provide


def censor(text, blacklist=()):
    output = []

    if not blacklist:
        blacklist = provide()

    for word in text.split(' '):
        if word in blacklist:
            output.append('*****')
        else:
            output.append(word)

    return ' '.join(output)


print(censor("You're a damn fool"))
