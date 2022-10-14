CREATE TABLE discussion (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	canonical VARCHAR(256) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (canonical)
);

CREATE TABLE user (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	nick VARCHAR(64) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nick)
);

CREATE TABLE comment (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	content VARCHAR(2048) NOT NULL, 
	reply_to_id INTEGER, 
	discussion_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(reply_to_id) REFERENCES comment (id), 
	FOREIGN KEY(discussion_id) REFERENCES discussion (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);

