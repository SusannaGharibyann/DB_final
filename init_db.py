from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройки подключения к базе данных
DATABASE_URL = "postgresql://pguser:pwd123@localhost:5432/my_database"

# Создаем объект Engine
engine = create_engine(DATABASE_URL, echo=True)

# Базовый класс для моделей
Base = declarative_base()

# Определяем таблицу как ORM-модель
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Добавляем данные в таблицу
try:
    # Пример добавления пользователей
    user1 = User(name="Alice", age=30)
    user2 = User(name="Bob", age=25)
    db.add(user1)
    db.add(user2)
    db.commit()

    print("Users added successfully.")

    # Пример запроса всех пользователей
    users = db.query(User).all()
    for user in users:
        print(f"User {user.id}: {user.name}, Age: {user.age}")

except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
