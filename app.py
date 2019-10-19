import os
from flask import Flask, render_template
from views.alerts import alert_bluprint
from views.stores import store_bluprint
from views.users import user_bluprint

app = Flask(__name__)
app.secret_key = 'aspwW9KtfpU6YyRWOgUk8kIWyXZSijwYqCeKyuILqJZyLQywCm547YvlG8porH6e'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(alert_bluprint, url_prefix='/alerts')
app.register_blueprint(store_bluprint, url_prefix='/stores')
app.register_blueprint(user_bluprint, url_prefix='/users')


if __name__ == '__main__':
    app.run(debug=True)
