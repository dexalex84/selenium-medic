text = "dfdfdf\n" \
       "fff\n" \
       "fff"

print(text)

print(text.find("\n"))
print(text[0:text.find("\n")])

text3='alsdfsdfdfgdfgsdex.'

print(text3[::-1])
print(text3[::-1].find("."))
print(text3[ - text3[::-1].find(".") - 1:])