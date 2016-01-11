![VerseCateBot](http://i.imgur.com/zzFkW5g.png)

**A reddit bot that posts Bible verses when asked to.**

* [Where It Runs](#where)
* [Usage](#usage)
  * [Making Verse Quotations](#making-verse-quotations)
  * [Setting a Default Translation](#setting-a-default-translation)
* [Authors](#authors)
* [License](#license)
* [Thanks](#thanks)

## WHERE
VerseCateBot runs only on the following public subreddits:

	* /r/Catholicism
	* /r/Christianity
	* /r/TelaIgne
	* /r/3OP
	* /r/DebateACatholic
	* /r/Judaism
	* /r/TrueChristian

## USAGE
### Making Verse Quotations
VerseCateBot is triggered by verse quotations on specific subreddits. Verse quotations are enclosed in brackets ([]), and may specify a desired translation within. A VerseCateBot quotation must follow one of the following formats (in each case the translation is optional):

```
[Book Chapter Translation]
[Book Chapter:Verse Translation]
[Book Chapter:StartVerse-EndVerse Translation]
```

### Setting a Default Translation
A default translation is the translation VerseCateBot defaults to for a particular subreddit. This means that a subreddit can specify a default translation, and the user(s) do not need to place the abbreviation for the translation within their comment.

Default translations for a subreddit can be set by sending a request to /u/kono_hito_wa (the operator of VerseCateBot). Either send a message to /u/kono_hito_wa or click the "Set Default Translation" link on a VerseCateBot response and request a default translation. These are not automatic. User /u/kono_hito_wa will manually make these changes. so it could take a while. Sorry for the inconvenice. This is really a combination of issue with the VerseBot code and my (/u/kono_hito_wa) time for this. I will respond to you when I receive your request, and I will respond to you when I have made the change, so don't stress out if you don't hear from me right away.

When requesting a default translation for a subreddit, the requester **must** be a moderator of the subreddit, otherwise I will simply ignore the request. Subreddit default translations never expire.

## AUTHORS
[kono_hito_wa](http://reddit.com/u/kono_hito_wa).
Derived from code written by [Matthieu Grieger](http://matthieugrieger.com), although the code at this point has been transffered to https://github.com/Team-VerseBot/versebot.

## LICENSE
	The MIT License (MIT)

	Copyright (c) 2014, 2015 Matthieu Grieger

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.

## THANKS
* [BibleGateway](http://www.biblegateway.com) and [Bible Hub](http://biblehub.com/) for being the sources of all texts posted by VerseCateBot.  
* [All those who contribute](https://github.com/praw-dev/praw/graphs/contributors) to [PRAW (Python Reddit API Wrapper)](https://github.com/praw-dev/praw).
* [Adam Grieger](https://github.com/adamgrieger) for the awesome VerseCateBot image at the top of this README.
