from yattag import Doc

doc, tag, text = Doc().tagtext()


with tag('html'):
    with tag('head'):
        doc.stag('link', rel='stylesheet', href='style.css')
    with tag('body'):
        with tag('p', id = 'main'):
            text('some text')
        with tag('a', href='/my-url', klass="test"):
            text('some link')

result = doc.getvalue()

f = open("index.html", 'w+')
f.write(result)
f.close()

print(result)