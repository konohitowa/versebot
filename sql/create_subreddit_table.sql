/*
  VerseBot for reddit
  By Matthieu Grieger
  create_subreddit_table.sql
  Copyright (c) 2015 Matthieu Grieger (MIT License)
*/

CREATE TABLE subreddit_stats (id SERIAL PRIMARY KEY, sub TEXT, count INTEGER DEFAULT 0, last_used TIMESTAMP WITH TIME ZONE DEFAULT NULL);
