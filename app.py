from src.server import create_app

app = create_app('src.config.DevelopmentConfig')

if __name__ == "__main__":
    app.run(host = "0.0.0.0",load_dotenv=True)
