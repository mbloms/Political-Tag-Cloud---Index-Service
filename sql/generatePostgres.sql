CREATE TABLE grp(
	groupId BIGINT PRIMARY KEY,
	name VARCHAR(40)
);
CREATE TABLE usr(
	userId BIGINT PRIMARY KEY
);
CREATE TABLE userInGroup(
	groupId BIGINT REFERENCES grp (groupId), 
	userId 	BIGINT REFERENCES usr (userId),
	PRIMARY KEY(groupId,userId)
);
