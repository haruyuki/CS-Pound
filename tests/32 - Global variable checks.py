
cooldown = False

def hi():
    cooldown = True
    print(cooldown)


def test():
    if not cooldown:
        print('not on cooldown')
        hi()
        print(cooldown)
    else:
        print('on cooldown')
    print(cooldown)

test()
print(cooldown)
test()
print(cooldown)