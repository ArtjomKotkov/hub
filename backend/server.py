import uvicorn

from backend import Logic, Entrypoints, Settings


def main():
    app_logic = Logic()
    app_logic.wire(modules=[__name__], packages=['backend.entrypoints'])

    entrypoints = Entrypoints()
    entrypoints.mount()

    uvicorn.run(entrypoints.fast_api, host=Settings.SERVER_HOST, port=int(Settings.SERVER_PORT))


if __name__ == '__main__':
    main()
