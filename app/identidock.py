import hashlib
import requests
import redis
from flask import Flask, Response, request

app = Flask(__name__)
salt = "UniqueSalt"
defaultName = 'Joe Bloggs'
cache = redis.StrictRedis(host='redis', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = defaultName

    saltedName = f'{salt}{name}'
    nameHash = hashlib.sha256(saltedName.encode()).hexdigest()

    header = '<html><head><title>Identidock</title></head>'
    body = F'''<body><form method="POST">
                Hello <input type="text" name="name" value="{name}">
                <input type="submit" value="submit">
                </form><p>You look like a:<img src="/monster/{nameHash}"/>'''
    footer = '</body></html>'

    return f'{header}{body}{footer}'


@app.route('/monster/<name>')
def getIdenticon(name):
    image = cache.get(name)
    if image is None:
        print('Cache miss', flush=True)
        r = requests.get(f'http://dnmonster:8080/monster/{name}?size=80')
        image = r.content
        cache.set(name, image)

    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
