from flaskr import create_app
app = create_app()

is_dev = False

if __name__ == "__main__":
    if is_dev:
        app.run(port=9447, debug=True)
    else:
        app.run(host='0.0.0.0', port=9447, debug=False)

