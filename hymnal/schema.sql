DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS hymns;

-- create a user table with id, username, and password --
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- create a hymn table with id, title, and content --
CREATE TABLE hymns (
  id SERIAL PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL
);
