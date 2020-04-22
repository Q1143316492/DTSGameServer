DROP TABLE user;
CREATE TABLE [user](
  [user_id] INTEGER PRIMARY KEY AUTOINCREMENT,
  [username] VARCHAR(20) NOT NULL UNIQUE, 
  [password] VARCHAR(20) NOT NULL, 
  [salt] CHAR(4) NOT NULL,
  [md5] CHAR(32));

INSERT INTO [user] (username, password, salt) 
       VALUES ("netease1", "123456", "qwer")
       
DELETE from [user];