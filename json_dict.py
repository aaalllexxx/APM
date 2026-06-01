"""
JsonDict — JSON-файл как Python-объект с автосохранением.
"""

import json
from contextlib import contextmanager


class JsonDict:
    """Класс для работы с JSON как с объектом.

    При изменении атрибутов значения сохраняются в файл.
    Поддерживает batch-режим для отложенной записи.

    Пример:
        data = JsonDict("config.json")
        data.host = "0.0.0.0"       # автоматически сохраняется
        print(data.port)             # читает из файла

        # Batch-режим (одна запись на диск вместо нескольких):
        with data.batch_update():
            data.host = "0.0.0.0"
            data.port = 8080
            data.debug = True
        # Данные записываются на диск один раз при выходе из блока
    """

    _INTERNAL_ATTRS = frozenset({"dictionary", "path", "encoding", "_dirty", "_batch_mode"})

    def __init__(self, path, encoding="utf-8"):
        self.path = path
        self.encoding = encoding
        self._dirty = False
        self._batch_mode = False
        self.dictionary = self.load()

    def __getitem__(self, item):
        self.dictionary = self.load()
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __setattr__(self, key, value):
        if "dictionary" in self.__dict__ and key not in self._INTERNAL_ATTRS:
            self.dictionary[key] = value
            self._dirty = True
            if not self._batch_mode:
                self._flush()
        self.__dict__[key] = value

    def _flush(self):
        """Записывает изменения на диск, если есть несохранённые данные."""
        if self._dirty:
            self.push(self.dictionary)
            self._dirty = False

    @contextmanager
    def batch_update(self):
        """Context manager для пакетного обновления.

        Откладывает запись на диск до выхода из блока with.

        Пример:
            with data.batch_update():
                data.host = "0.0.0.0"
                data.port = 8080
            # Одна запись на диск
        """
        self._batch_mode = True
        try:
            yield
        finally:
            self._batch_mode = False
            self._flush()

    def keys(self) -> list:
        return list(self.dictionary)

    def load(self) -> dict:
        with open(self.path, "r", encoding=self.encoding) as file:
            content = file.read()
            if not content:
                content = "{}"
            dictionary = json.loads(content)

        for k, v in dictionary.items():
            self.__setattr__(k, v)

        return dictionary

    def push(self, data: dict) -> None:
        data = json.dumps(data, indent=2)
        with open(self.path, "w", encoding=self.encoding) as file:
            file.write(data)

    def delete_item(self, key: str) -> None:
        dictionary = self.load()
        del dictionary[key]
        self.push(dictionary)

    def get(self, key: str):
        return self.dictionary.get(key)

    def __repr__(self):
        self.dictionary = self.load()
        return json.dumps(self.dictionary, indent=2)
