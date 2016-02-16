CREATE TABLE grp(
	groupId BIGINT PRIMARY KEY,
	name VARCHAR(50)
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
	timestamp TIMESTAMP,
	content VARCHAR(160),
	location VARCHAR(30)
);
CREATE TABLE retweet(
	tweetId BIGINT REFERENCES tweet (tweetId) PRIMARY KEY,
	creatorId BIGINT,
	originalTweetId BIGINT
);
CREATE TABLE mention(
	mentionId SERIAL PRIMARY KEY,
	userId BIGINT UNIQUE
);
CREATE TABLE tweetMention(
	tweetId BIGINT REFERENCES tweet (tweetId),
    mentionId INT REFERENCES mention (mentionId),
    PRIMARY KEY(tweetId,mentionId)
);
CREATE TABLE tag(
	tagId SERIAL PRIMARY KEY,
	tag   VARCHAR(40) UNIQUE
);
CREATE TABLE tweetTag(
	tweetId BIGINT REFERENCES tweet (tweetId),
	tagId INT REFERENCES tag (tagId),
	PRIMARY KEY(tweetId,tagId)
);


SELECT to_timestamp('Mon Mar 26 19:25:48 +0000 2007','Dy Mon DD HH24:MI:SS xxxx YYYY') FROM usr LIMIT 1