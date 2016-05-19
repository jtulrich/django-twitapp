--
-- These are convenience functions for PostgreSQL for use
--   in the Twitapp project.
--

CREATE OR REPLACE FUNCTION GetMostRetweetedTweetByDay()
  RETURNS TABLE (
		id text,
		tweet_text text,
		tweet_latitude double precision,
		tweet_longitude double precision,
		tweet_date timestamp with time zone,
    tweet_retweets integer,
		user_screen_name text)
	AS $$
	SELECT tweet_id,
          "text",
          user_location_latitude,
          user_location_longitude,
          date_trunc('day', created_at),
          retweet_count,
          user_screen_name
	  FROM twit_tweet,
          (
            SELECT t.id as tid,
              max_retweets.tday as tday
              FROM twit_tweet as t,
                    (
                    SELECT date_trunc('day', created_at) as tday, MAX(retweet_count) as tre
                      FROM twit_tweet
                     WHERE retweet_original = TRUE
                     GROUP BY date_trunc('day', created_at)
                    ) as max_retweets
             WHERE max_retweets.tday = date_trunc('day', t.created_at)
               AND max_retweets.tre = t.retweet_count
               AND t.retweet_original = TRUE
               AND t.id = (SELECT id
                             FROM twit_tweet
                            WHERE retweet_original = TRUE
                              AND max_retweets.tday = date_trunc('day', created_at)
                              AND max_retweets.tre = retweet_count
                            ORDER BY created_at DESC
                            LIMIT 1)
          ) as retweet_group
	 WHERE twit_tweet.id = retweet_group.tid
	 ORDER BY date_trunc('day', created_at) asc
 $$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION GetTweetsGroupedByHourMasterRecords()
  RETURNS TABLE (
           id timestamp with time zone,
           tweet_hour timestamp with time zone,
           tweet_hour_count bigint,
           tweet_user text,
           tweet_text text,
           tweet_latitude double precision,
           tweet_longitude double precision,
           tweet_score_type text,
           tweet_score integer)
  AS $$
  SELECT count_group.tweet_hour,
          count_group.tweet_hour,
          count_group.tweet_hour_count,
          twit_tweet.user_screen_name,
          twit_tweet.text,
          twit_tweet.user_location_latitude,
          twit_tweet.user_location_longitude,
          CASE WHEN retweet_group.thour IS NOT NULL THEN 'retweets'
               WHEN favorite_group.thour IS NOT NULL THEN 'favorites'
               ELSE '-' END as score_type,
          CASE WHEN retweet_group.thour IS NOT NULL THEN twit_tweet.retweet_count
               WHEN favorite_group.thour IS NOT NULL THEN twit_tweet.favorite_count
               ELSE 0 END as score_value
	  FROM twit_tweet
          LEFT OUTER JOIN
          (
            SELECT t.id as tid,
              max_retweets.thour as thour
              FROM twit_tweet as t,
              (
              SELECT date_trunc('hour', created_at) as thour, MAX(retweet_count) as tre
                FROM twit_tweet
               WHERE retweet_original = TRUE
               GROUP BY date_trunc('hour', created_at)
              ) as max_retweets
             WHERE max_retweets.thour = date_trunc('hour', t.created_at)
               AND max_retweets.tre = t.retweet_count
               AND t.retweet_original = TRUE
               AND t.id = (SELECT id
                 FROM twit_tweet
                WHERE retweet_original = TRUE
                  AND max_retweets.thour = date_trunc('hour', created_at)
                  AND max_retweets.tre = retweet_count
                ORDER BY created_at DESC
                LIMIT 1)
          ) as retweet_group ON twit_tweet.id = retweet_group.tid
          LEFT OUTER JOIN
          (
            SELECT t.id as tid,
              max_favorites.thour as thour
              FROM twit_tweet as t,
              (
              SELECT date_trunc('hour', created_at) as thour, MAX(favorite_count) as tfav
                FROM twit_tweet
               GROUP BY date_trunc('hour', created_at)
              ) as max_favorites
             WHERE max_favorites.thour = date_trunc('hour', t.created_at)
               AND max_favorites.tfav = t.favorite_count
               AND t.id = (SELECT id
                 FROM twit_tweet
                WHERE max_favorites.thour = date_trunc('hour', created_at)
                  AND max_favorites.tfav = favorite_count
                ORDER BY created_at DESC
                LIMIT 1)
          ) as favorite_group ON twit_tweet.id = favorite_group.tid,
          (
            SELECT date_trunc('hour', created_at) as tweet_hour,
              COUNT(*) as tweet_hour_count
              FROM twit_tweet
             GROUP BY date_trunc('hour', created_at)
          ) as count_group
	 WHERE count_group.tweet_hour = date_trunc('hour', twit_tweet.created_at)
  $$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION GetTweetsGroupedByHourWithHighestValues()
	RETURNS TABLE (
	         id timestamp with time zone,
           tweet_hour timestamp with time zone,
           tweet_hour_count bigint,
           tweet_user text,
           tweet_text text,
           tweet_latitude double precision,
           tweet_longitude double precision,
           tweet_score_type text,
           tweet_score integer)
	AS $$
	SELECT mr1.*
	  FROM (SELECT * FROM GetTweetsGroupedByHourMasterRecords()) as mr1
	 WHERE mr1.tweet_score_type = 'retweets'
      OR (mr1.tweet_score_type = 'favorites' 
          AND mr1.tweet_hour NOT IN (SELECT tweet_hour
                                       FROM GetTweetsGroupedByHourMasterRecords()
                                      WHERE tweet_score_type = 'retweets'));
 $$ LANGUAGE SQL;
