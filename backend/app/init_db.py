from datetime import datetime

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Course, User
from app.security import hash_password


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_SALT = "cms_admin_salt_2026"


COURSE_SEED = [
    {
        "code": "NOTICE",
        "category": "公告",
        "name": "CHATGPT工具网站",
        "url": "https://openai.com",
        "price": 0,
    },
    {
        "code": "DOCS",
        "category": "资料",
        "name": "收集整理的一些书籍和软件，免费分享给大家，点击课程链接即可获取",
        "url": "https://example.com/docs",
        "price": 0,
    },
    {
        "code": "AD-01",
        "category": "Android",
        "name": "5G时代必备 音视频WebRTC实时互动直播技术入门与实战",
        "url": "https://example.com/ad-01",
        "price": 8,
    },
    {
        "code": "AD-02",
        "category": "Android",
        "name": "Android 工程师（金职位）",
        "url": "https://example.com/ad-02",
        "price": 30,
    },
    {
        "code": "AD-03",
        "category": "Android",
        "name": "Android架构师之路 网络层架构设计与实战",
        "url": "https://example.com/ad-03",
        "price": 5,
    },
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        now = datetime.now()
        admin = db.scalar(select(User).where(User.username == ADMIN_USERNAME))
        if admin is None:
            db.add(
                User(
                    username=ADMIN_USERNAME,
                    password=hash_password(ADMIN_SALT, ADMIN_PASSWORD),
                    age=None,
                    salt=ADMIN_SALT,
                    create_time=now,
                    creator="system",
                    modify_time=now,
                    modifier="system",
                )
            )

        for item in COURSE_SEED:
            exists = db.scalar(select(Course).where(Course.code == item["code"]))
            if exists is None:
                db.add(
                    Course(
                        **item,
                        create_time=now,
                        creator="system",
                        modify_time=now,
                        modifier="system",
                    )
                )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized. Admin account: admin / admin123")
