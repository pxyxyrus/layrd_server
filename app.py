import server
import config

if __name__ == '__main__':
    
    app = server.create_app()
    app.run('localhost', 5001, True)