DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS menuicon;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS order_course;
DROP TABLE IF EXISTS 'order';

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,

  is_admin BOOLEAN DEFAULT false
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE menuicon (
  hashname TEXT PRIMARY KEY
);

CREATE TABLE course (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  title TEXT NOT NULL,
  description TEXT NOT NULL,
  icon_hashname TEXT NOT NULL DEFAULT 'default.png',

  price DECIMAL(10, 2) NOT NULL,

  status TEXT NOT NULL, /* on, off */

  created_by INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by INTEGER NOT NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (created_by) REFERENCES user (id),
  FOREIGN KEY (updated_by) REFERENCES user (id)
);

CREATE TABLE order_course (
  order_id INTEGER ,
  course_id INTEGER ,

  title TEXT NOT NULL,
  description TEXT NOT NULL,
  icon_hashname TEXT,

  price DECIMAL(10, 2) NOT NULL,
  quantity INTEGER NOT NULL,

  PRIMARY KEY (order_id, course_id),
  FOREIGN KEY (order_id) REFERENCES 'order' (id),  
  FOREIGN KEY (course_id) REFERENCES user (id)   
);

CREATE TABLE 'order' (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  status TEXT NOT NULL, /* new, confirmed, cancelled, finished */

  price DECIMAL(10, 2),

  table_no INTEGER NOT NULL DEFAULT 0, /* 0 means take out */
  take_out_address TEXT DEFAULT NULL, /* */
  take_out_phone_no TEXT DEFAULT NULL,

  created_by INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by INTEGER NOT NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (created_by) REFERENCES user (id)
);

INSERT INTO user (
  username, password, is_admin
) VALUES (
  'admin',
  'pbkdf2:sha256:50000$9kA3XtO5$260400438fdf448540971595b4bb9ad8d57c0afa07e627d63871cf16b2027032',
  1
), (
   'user',
   'pbkdf2:sha256:50000$gxO1YJ6g$d54b5972ec8e580fb0d7dc98648d79268eb73aa6f08d7a4a8300434e7ecaf814',
   0
);

INSERT INTO menuicon (
  hashname
) VALUES (
  'default.png'
), (
  'rice.png'
), (
  'fried_egg.png'
);
