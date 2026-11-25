import json
from typing import Dict
import redis


class RedisClient:
    def __init__(self, host: str, port: int, password: str, cert_path: str) -> None:
        self._client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            ssl=True,
            ssl_ca_certs=cert_path
        )

    def set(self, k: str, v: Dict) -> None:
        self._client.set(k, json.dumps(v, ensure_ascii=False))

    def get(self, k: str) -> Dict:
        result = self._client.get(k)
        if not result:
            return {}
        return json.loads(result.decode("utf-8"))

    def delete(self, k: str) -> int:
        """Удаляет ключ. Возвращает 1, если ключ существовал, иначе 0."""
        return self._client.delete(k)

    def keys(self, pattern: str = "*") -> list:
        """Возвращает список ключей, соответствующих паттерну (через SCAN)."""
        return [key.decode("utf-8") for key in self._client.scan_iter(match=pattern)]
# === Пример использования (для теста, потом закомментировать) ===
if __name__ == "__main__":
    client = RedisClient(
        host="c-c9qjhf4uimga8imabeos.rw.mdb.yandexcloud.net",
        port=6380,
        password=r"ycIm~`AU1\D(Vc|&Z8{}mrq0MCQgfX\<CCJB",
        cert_path=r"E:\RootCA.pem",
    )

   # 1. Печатаем ключи ДО — чтобы видеть исходное состояние
    print("Ключи до:", client.keys("test:*"))

    # 2. Запись
    client.set("test:user:1", {"name": "Иван", "age": 30})

    # 3. Чтение
    data = client.get("test:user:1")
    print("Прочитано:", data)

    # 4. Печатаем ключи ПОСЛЕ записи
    print("Ключи после записи:", client.keys("test:*"))

    # 5. Удаление временного ключа
    deleted = client.delete("test:user:1")
    print("Удалено (1 = был, 0 = не было):", deleted)

    # 6. Проверяем, что ключ действительно исчез
    print("Прочитано после удаления:", client.get("test:user:1"))  # {}

    # 7. Печатаем все оставшиеся ключи
    print("Все ключи после удаления:", client.keys("*"))