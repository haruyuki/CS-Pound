

REDACTED
# Encrypted = REDACTED

# ENCRYPTION
x = 'REDACTED'
x = [x[d:d+2] for d in range(0, len(x), 2)]  # Split into every 2 characters
s = '0123456789abcdef'
final_list = []
for i in range(len(x)):
    hex_string = '0x' + x[i]
    hex_value = int(hex_string, 16)
    flipped_value = abs(int(hex_value) - 256)
    formatted_value = format(int(flipped_value), '02x')
    formatted_value = list(formatted_value)
    for j in range(len(formatted_value)):
        formatted_value[j] = s[s.find(formatted_value[j]) - 6]
    rewinded_value = ''.join(map(str, formatted_value))
    final_list.append(rewinded_value)

final = ''.join(map(str, final_list))
print(final)

# Decryption
x = 'REDACTED'
y = [x[d:d+2] for d in range(0, len(x), 2)]
x = list(x)
s = '0123456789abcdef'
original_list = []
temp = []
for i in range(len(x)):
    forwarded_value = s[(s.find(x[i]) + 6) % 16]
    temp.append(forwarded_value)

x = ''.join(map(str, temp))
x = [x[d:d+2] for d in range(0, len(x), 2)]
for i in range(len(x)):
    hex_string = '0x' + x[i]
    hex_value = int(hex_string, 16)
    flipped_value = abs(int(hex_value) - 256)
    original_value = format(int(flipped_value), 'x')
    original_list.append(original_value)

original = ''.join(map(str, original_list))
print(original)  # REDACTED

'''
SPLIT INTO 2
['77', '64', 'ba', '66', 'fb', 'f9', '52', '3']

aloha = [x[d:d+2] for d in range(0, len(x), 2)]

0xKEY
119 100 186 102 251 249 82 3

for i in range(len(x)):
    value = '0x' + x[i]
    u = int(value, 16)
    aloha.append(u)


MINUS NEW - 256 (ABSOLUTE VALUE)
137 156 70 154 5 7 174 253

for i in range(len(x)):
    u = abs(int(x[i]) - 256)
    print(u, end=' ')


FORMAT
89 9c 46 9a 05 07 ae fd

for i in range(len(x)):
    print(format(int(x[i]), '02x',), end=' ')


COMBINE
899c469a0507aefd

''.join(x)

GO BACK 6 CHARACTERS
REDACTED

for i in range(len(x)):
    print(s[s.find(x[i]) - 6], end='')

DECRYPTION

REDACTED

ADD 6 CHARACTERS
s[(s.find('5') + 6) % 16]

SPLIT EVERY 2
899c469a0507aefd

[x[d:d+2] for d in range(0, len(x), 2)]

UNFORMAT
137 156 70 154 5 7 174 253

for i in range(len(x)):
    temp = '0x' + x[i]
    print(int(temp, 16), end = ' ')

MINUS NEW - 256 (ABS)
119 100 186 102 251 249 82 3

for i in range(len(x)):
    u = abs(int(x[i]) - 256)
    print(u, end=' ')

FORMAT
REDACTED

for i in range(len(x)):
    print(format(int(x[i]), 'x'),end='')
'''



REDACTED
# Encrypted: REDACTED

REDACTED
REDACTED








for i in range(len(x)):
    print(str(int(x[i]) - 12), end=' ')