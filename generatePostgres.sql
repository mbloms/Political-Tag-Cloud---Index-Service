CREATE TABLE grp(
	groupId SERIAL PRIMARY KEY,
	name VARCHAR(40),
	UNIQUE(name)
);
CREATE TABLE usr(
	userId BIGINT PRIMARY KEY
);
CREATE TABLE userInGroup(
	groupId INT REFERENCES grp (groupId), 
	userId 	BIGINT REFERENCES usr (userId),
	PRIMARY KEY(groupId,userId)
);
