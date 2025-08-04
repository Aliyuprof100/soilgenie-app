
from . import create_app  # The dot means "from the current package"

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)