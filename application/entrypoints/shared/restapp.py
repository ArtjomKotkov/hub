from __future__ import annotations

from typing import Callable

from fastapi import FastAPI, APIRouter, Depends

__all__ = [
    'RestApp',
]


class RestApp:
    sub_apps: list[tuple[str, type[RestApp]]] = []
    routers: list[tuple[str, APIRouter]] = []
    middlewares: list[type] = []
    exception_handlers: list[tuple[type[Exception], Callable]] = []
    dependencies: list[Depends] = []
    propagate_exception_handlers: bool = True

    def __init__(
        self,
        depth: int = 0,
        path: str = '/',
    ):
        self._depth = depth
        self._path = path

        self._propagated_exception_handlers: list[tuple[type[Exception], Callable]] = []
        self._fast_api_app = FastAPI(dependencies=self.dependencies)

    def _make_app(self) -> None:
        for conf in self.routers:
            prefix, router = conf

            print(f'\033[94m{"  "*(self._depth+1)}{prefix if prefix != "" else "/"}\033[00m')
            for route in router.routes:
                print(f'{"  "*(self._depth+2)}{route.path} - {route.name} - [{",".join(route.methods)}]')
            self._fast_api_app.include_router(router, prefix=prefix)

        for middleware in self.middlewares:
            self._fast_api_app.add_middleware(middleware)

        for conf in self.exception_handlers:
            exc, handler = conf
            self._fast_api_app.add_exception_handler(exc, handler)

        for conf in self._propagated_exception_handlers:
            exc, handler = conf
            self._fast_api_app.add_exception_handler(exc, handler)

    def do_propagate_exception_handlers(self, handlers: list[tuple[type[Exception], Callable]]) -> None:
        self._propagated_exception_handlers.extend(handlers)

    def mount(self) -> None:
        self._print_api()

        self._make_app()

        for conf in self.sub_apps:
            path, factory = conf

            app = factory(self._depth + 1, path)
            fast_api_app = app.fast_api
            self._fast_api_app.mount(path, fast_api_app)

            if self.propagate_exception_handlers:
                app.do_propagate_exception_handlers(self.exception_handlers)
                app.do_propagate_exception_handlers(self._propagated_exception_handlers)

            app.mount()

    @property
    def fast_api(self) -> FastAPI:
        return self._fast_api_app

    def _print_api(self) -> None:
        if self._depth == 0:
            print('Enabled api schema:')
        print(self)

    def __repr__(self):
        return f'\033[92m{"  "*self._depth}{self._path}\033[00m - \033[93m{self.__class__.__name__}\033[00m'
