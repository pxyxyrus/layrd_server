import server
import config

app = server.create_app()

if __name__ == "__main__":
    app.run('localhost', 5001, True)