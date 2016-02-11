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
CREATE TABLE tweet(
	tweetId BIGINT PRIMARY KEY, 
	userId 	BIGINT REFERENCES usr (userId),
	timestamp VARCHAR(30),
	content VARCHAR(140)
);
CREATE TABLE tweetTag(
	tweetId BIGINT REFERENCES tweet (tweetId),
	tag VARCHAR(30),
	PRIMARY KEY(tweetId,tag)
);
