DROP TABLE user;
CREATE TABLE [user](
  [user_id] INTEGER PRIMARY KEY AUTOINCREMENT,
  [username] VARCHAR(20) NOT NULL UNIQUE, 
  [password] VARCHAR(20) NOT NULL, 
  [salt] CHAR(4) NOT NULL,
  [md5] CHAR(32));
  
CREATE TABLE [user_level](
  [user_id] INTEGER PRIMARY KEY, 
  [level] INT);

INSERT INTO [user] (username, password, salt, md5) 
       VALUES ("netease1", "123456", "qwer", "b5b037a78522671b89a2c1b21d9b80c6")
       
UPDATE [user] 
SET password = ?
WHERE username = ?

DELETE from [user];