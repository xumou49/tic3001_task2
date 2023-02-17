from application.app import init_app
from config import BaseConfig

app, _ = init_app(BaseConfig)

if __name__ == '__main__':
    app.run(debug=True)
