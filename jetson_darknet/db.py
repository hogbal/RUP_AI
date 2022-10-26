# from sqlalchemy import create_engine, Column, String, Integer
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# engine = create_engine("mariadb+mariadbconnector://root:root@hogbal.iptime.org:3306/rup_db")
# Base = declarative_base()

# class user_info(Base):
#     __tablename__ = "USER_INFO"
#     UID = Column(String(length=40), primary_key=True)
#     Password = Column(String(length=15), unique=True)
#     Nickname = Column(String(length=20))
#     Sex = Column(String(length=20), nullable=False)
#     Birth = Column(String(length=10), nullable=False)
#     Profile_photo_url = Column(String(length=100))
#     College = Column(String(length=100))
#     Major = Column(String(length=100))
#     Point = Column(Integer, default=0)
#     Count_recyle = Column(Integer, default=0)
    
# Base.metadata.create_all(engine)

# Session = sessionmaker()
# Session.configure(bind=engine)
# session = Session()

# usr = session.query(user_info).get("0")
# usr.Point = usr.Point+1
# session.commit()

while(True):
    test = input()
    print(test)