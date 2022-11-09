CREATE TABLE USER_INFO(
    UID VARCHAR(40),
    Email VARCHAR(40) NOT NULL UNIQUE,
    Password VARCHAR(15),
    Nickname VARCHAR(20),
    Sex VARCHAR(10) NOT NULL,
    Birth VARCHAR(10) NOT NULL,
    Profile_photo_url VARCHAR(100),
    College VARCHAR(100),
    Major VARCHAR(100),
    Point INT DEFAULT 0,
    Count_recyle INT DEFAULT 0,
    primary key(UID)
);

INSERT INTO USER_INFO VALUES ("0", "hogbal31@gmail.com", "hogbal", "hogbal","Man","990618","asdf","Donga-A","computer",0,0);
INSERT INTO USER_INFO VALUES ("1", "pthdud1123@naver.com", "pthdud1123", "pthdud1123","Woman","991123","asdf","Donga-A","computer",0,0);