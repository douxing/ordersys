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
  quantity INTEGER NOT NULL DEFAULT 0,

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

  status TEXT NOT NULL, /* new, cancelled, finished */

  price DECIMAL(10, 2),

  table_no INTEGER, /* NULL means take out */
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
  'hello',
  'pbkdf2:sha256:50000$Y6nJa6BB$c0ec5d899189cc4085891d06823b16695c509c435a7e8cc1498df3364bbf7d6d',
  1
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
