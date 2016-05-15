--
-- These are convenience functions for PostgreSQL for use
--   in the Twitapp project.
--

CREATE OR REPLACE FUNCTION GetMostRetweetedTweet()
  RETURNS TABLE (
		id text,
		tweet_text text,
		tweet_latitude double precision,
		tweet_longitude double precision,
		tweet_date timestamp with time zone,
		user_screen_name text)
	AS $$
	SELECT "tweet_id",
		"text",
		"user_location_latitude",
		"user_location_longitude",
		"created_at",
		"user_screen_name"
	  FROM twit_tweet
	 ORDER BY retweet_count desc
	 LIMIT 1
 $$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION GetMostRetweetedTweetForDayHour(target_date timestamp with time zone)
  RETURNS TABLE (
		id text,
		tweet_text text,
		tweet_latitude double precision,
		tweet_longitude double precision,
		tweet_hour timestamp with time zone,
		user_screen_name text)
	AS $$
	SELECT "tweet_id",
		"text",
		"user_location_latitude",
		"user_location_longitude",
		target_date,
		"user_screen_name"
	  FROM twit_tweet
	 WHERE date_trunc('hour', "created_at") = target_date
	 ORDER BY retweet_count desc
	 LIMIT 1
 $$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION GetTweetsGroupedByHour()
  RETURNS TABLE (
		id timestamp with time zone,
		tweet_hour timestamp with time zone,
		tweet_hour_count bigint)
	AS $$
	SELECT date_trunc('hour', "created_at"),
		date_trunc('hour', "created_at"),
		count(*)
	  FROM twit_tweet
	 GROUP BY date_trunc('hour', "created_at")
	 ORDER BY date_trunc('hour', "created_at") asc
 $$ LANGUAGE SQL;


--
-- This doesn't deal with a number of possible data issues, but I can't even right now.
--
DROP FUNCTION GetTweetsGroupedByHourWithMostRetweeted();
CREATE OR REPLACE FUNCTION GetTweetsGroupedByHourWithMostRetweeted()
	RETURNS TABLE (
	         id timestamp with time zone,
		 tweet_hour timestamp with time zone,
		 tweet_hour_count bigint,
		 tweet_user text,
		 tweet_text text,
		 tweet_latitude double precision,
		 tweet_longitude double precision,
		 tweet_retweets integer)
	AS $$
	SELECT regrouper.tweet_hour,
	        regrouper.tweet_hour,
		regrouper.tweet_hour_count,
		twit_tweet.user_screen_name,
		twit_tweet.text,
		twit_tweet.user_location_latitude,
		twit_tweet.user_location_longitude,
		twit_tweet.retweet_count
	  FROM twit_tweet,
	       (
		SELECT date_trunc('hour', "created_at") as tweet_hour, COUNT(*) as tweet_hour_count, MAX(retweet_count) as max_re
		  FROM twit_tweet
		 GROUP BY date_trunc('hour', "created_at")
	       ) as regrouper
	 WHERE date_trunc('hour', twit_tweet.created_at) = regrouper.tweet_hour
	   AND retweet_count = regrouper.max_re
 $$ LANGUAGE SQL;
