CREATE TABLE grp(
	groupId SERIAL PRIMARY KEY,
	name VARCHAR(50)
);
CREATE TABLE usr(
	userId BIGINT PRIMARY KEY
);
CREATE TABLE userInGroup(
	groupId INT REFERENCES grp (groupId), 
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
/* creatorId and originalTweetId is not foreign keys of usr since we want to be able to handle retweets from users that are not in our database*/
CREATE TABLE retweet(
	tweetId BIGINT REFERENCES tweet (tweetId) PRIMARY KEY,
	creatorId BIGINT,
	originalTweetId BIGINT
);

/* userId is not a foreign key so that we can handle mentions with users that is not in our database */
CREATE TABLE tweetMention(
	tweetId BIGINT REFERENCES tweet (tweetId),
    userId BIGINT,
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
CREATE TABLE following(
	followedId BIGINT REFERENCES usr(userId),
	followerId BIGINT REFERENCES usr(userId),
	PRIMARY KEY(followedId, followerId)
);

CREATE TABLE unfollow(
	unfollowId SERIAL PRIMARY KEY,
	followedId BIGINT REFERENCES usr(userId),
	followerId BIGINT REFERENCES usr(userId),
	timestamp TIMESTAMP
);

CREATE TABLE startfollow(
	unfollowId SERIAL PRIMARY KEY,
	followedId BIGINT REFERENCES usr(userId),
	followerId BIGINT REFERENCES usr(userId),
	timestamp TIMESTAMP
);


