from my_app import create_app
from threading import Timer
import webbrowser


app = create_app()

def abrir_navegador():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, abrir_navegador).start()
    app.run()