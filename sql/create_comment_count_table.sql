/*
  VerseBot for reddit
  By Matthieu Grieger
  create_comment_count_table.sql
  Copyright (c) 2015 Matthieu Grieger (MIT License)
*/

CREATE TABLE comment_count (id SERIAL PRIMARY KEY, count INTEGER DEFAULT 0, last_used TIMESTAMP WITH TIME ZONE DEFAULT NULL);
INSERT INTO comment_count DEFAULT VALUES;
