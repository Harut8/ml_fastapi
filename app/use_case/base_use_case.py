from adapters.spi.base_repo import BaseRepository


class BaseUseCase:
    def __init__(self, base_repo: BaseRepository):
        self._base_repo = base_repo

    @classmethod
    def factory(cls: type, **kwargs):
        return cls(**kwargs)

    @property
    def base_repo(self):
        return self._base_repo
