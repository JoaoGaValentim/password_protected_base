from datetime import datetime
from pathlib import Path


class BaseModel:
    BASE_DIR = Path(__file__).parent.parent
    DB_DIR = BASE_DIR / "db"

    def save(self):
        table_path = Path(self.DB_DIR / f"{self.__class__.__name__}.txt")
        if not table_path.exists():
            table_path.touch()

        with open(table_path, "a") as file:
            file.write("|".join(list(map(str, self.__dict__.values()))))
            file.write("\n")

    @classmethod
    def get(cls):
        table_path = Path(cls.DB_DIR / f"{cls.__name__}.txt")
        if not table_path.exists():
            table_path.touch()

        with open(table_path, "r") as file:
            data_file = file.readlines()

        data = []
        attrs = vars(cls())

        for i in data_file:
            splited_data = i.split("|")
            zipped_data = zip(attrs, splited_data)
            tmp_dict = dict(zipped_data)
            data.append(tmp_dict)

        return data


class Password(BaseModel):
    def __init__(self, domain=None, password=None, expires=False):
        super().__init__()
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()


password = Password(
    domain="github.com",
    password="123456",
)

password.get()
