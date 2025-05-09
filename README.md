# reddit-search-engine
A python based reddit scraper utilizing PyLucene and Flask

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

 
 ## Overview of the System
 ### Architecture
 This project utilizes the PRAW library to connect with the APIs and make proper calls for retrieving Reddit post data. The  crawler program is written in Python and consists of four modules: `main.py`, `RedditAuth.py`, `Fetch_Process_Data.py`, and `DataStorer.py`. These files work together to authenticate with Reddit, fetch posts, process the fetched data, and store them in JSON files. The web_ui includes: `PyLucene.py`, `app.py`, `index.html`, `results.html`, `webUI_styling.css`. These files work together to index the crawled data by field stored in the JSON objects  using PyLucene. Then using Flask, a local web application was created to rank the documents and return results based on the user inputted query.

 ### Module Breakdown
 1. `main.py`: This is the main file of the crawler application. The main file imports all of the other files and modules and their methods. It initializes data storage, authenticates the user’s session, defines which specific subreddits to crawl, fetches the posts of the specified subreddits, processes the data, and then stores it into JSON files.
 2. `RedditAuth.py`: handles the authentication of a session with Reddit and makes API calls via the PRAW library. It fetches the necessary credentials from the new team Reddit account created and authenticates the account with Reddit, returning a newly created session.
 3. `Fetch_Process_Data.py`: handles two specific functions. Firsty, it fetches the posts from the specified subreddits. Then, it processes the posts. Via PRAW, the module retrieves posts and uses requests and BeatifulSoup to scrape and process the retrieved data. It cleans the HTML data and formats it into organizes JSON data.
 4. `DataStorer.py`: in charge of storing the processed data. It checks the data limits and data volume, then write the data into `CrawledData` directory the user specifies. 
 5. `PyLucene.py`: initializes a Lucene environment and creates an index from the JSONL files that were created storing the raw data from the Reddit crawler. It iterates over the JSONL files stored in the `CrawledData` directory, processing each line as a JSON object and indexing the various fields. This sets up efficient retrieval of posts within the web app. 
 6. `App.py`: uses Flask to provide a web-based search interface that allows users to query and retrieve posts from the indexed data, ranked according to their preferences. It initializes Lucene and the JVM, opening the specified directory where the indexed data lives and creates and `IndexSearcher` and `StandardAnalyzer` to facilitate search queries. It provides two options for search and rankingl the default PyLucene ranking (BM25) and a `custom_score()` function which calculates a combined score based on votes, and normalized timestamp, allowing for flexible ranking based on different weights for relevance, votes, and recency. The search results are retrieved, adn the top 10 results are scored using either the default BM25 score or the custom score. 
 7. `index.html`: contains the HTML code to create the search interface for this project. It includes a form-like structure where users cna input their search query and select their preferred ranking option. If the `Custom Score` ranking option is selected, the additional drop-down fields appear allowing users to specify weights for sorting by relevance, votes, and time. The UI is styled with CSS and JavaScript, used to show or hide the custom options based on the selected ranking options.
 8. `results.html`: contains the HTML code to create the search engine's results page. It displays the top search results for the user's query, showing detaisl such as the titles, user, body, URL, votes, and score for each result. Lastly, there is a 'Back to Search' button for the user to return to the search engine that `index.html` provides.
 9. `webUI_styling.css`: the code just styles the elements of the webpage to create a clean and centered layout. It also sets fonts, widths of buttons, text fields, etc.

### Index Structures
#### Fields Used:
1. Text Field: Title & Body
     - The title is used for indexing for full-text search and is stored for retrieval.
     - The body stores the content of the document, it is also indexed for full-text search and stored for retrieval.
2. String Field: URL & User
    - URL is indexed and stored so it can be used for exact match queries.
    - The user is indexed and stored so it can be used for exact match queries.
3. Stored Field: Linked Title
    - Linked Title stores the title of the document being linked to.
4. Intpoint: Votes
    - Votes are being stored and indexed for the range of queries.
5. LongPoint: Timestamp
    - Timestamp is being stored and indexed for the range of queries.

The selected analyzers are Lucene's StandardAnalyzer. This analyzer divides the text into individual words based on the standard tokenization rules, eliminates common English stop words, and converts all tokens to lowercase. 

### Search Algorithm
The querying process harnesses the power of Lucene's scoring mechanism, which
seamlessly integrates the Vector Space Model (VSM) of Information Retrieval and the Boolean
model. Initially, Lucene's StandardAnalyzer preprocesses documents, ensuring compatibility
with the VSM by converting text into lowercase tokens and eliminating common stop words. It
then employs the Lucene IndexSearcher to navigate through indexed documents, aligning with
the Boolean model's principles by filtering relevant documents based on boolean logic in query
specifications. As the search progresses, Lucene's scoring algorithm combines elements from
both models: the VSM's consideration of term frequency and inverse document frequency, and
the Boolean model's logical operations to narrow down the set of documents to be scored. This
fusion of VSM and Boolean model principles allows Lucene to determine the relevance of each
document to the user's query accurately. Lucene will then combine these various elements into a
final score. Also attempted allowing users to order posts by votes, time,
relevance, and or a combination of them via our custom scoring method which incorporates the
time and relevance of the Reddit document via the age of the post and the number of votes.

### Web Framework
The search engine’s backend runs on Python scripts with the front end being a
simplistic UI designed with HTML, CSS Javascript. The app is hosted locally using a flask
server running on port 8080. The only other script aside from the flask server is a PyLucene.py.
This is a utility script that is run manually rather than concurrently with the server and is used to
index the JSON data retrieved by the crawler.

## Limitations of the System
Reddit’s API limits how fast & much data can be obtained via crawling due to restricting us if you
don’t use the developer version of Reddit. The information that can be obtained from Reddit is
limited to posts, comments, and user profiles which means the quality of the data could be
questionable. Reddit is very volatile and dynamic with how new content is being added via posts,
comments, and votes. This could prove to be a problem when you want to ensure the data that you
crawl stays relevant. Reddit contains a vast amount of different data via text, images, videos, and
links which means that I need to create a more complex method to read these different data.

## Deployment
**Crawler**:

- Add your `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT` as environment variables
- Check python files for correct paths
- Run either `main.py` or `crawler.sh` in the `/crawler/` directory

**Web UI**:
- Enter the `/web_ui/` directory
- Update the path to `app.py` in `indexer.sh`
- Update the correct paths in `app.py`
- Run `indexer.sh`

** The web application runs on simple HTML code with CSS web-styling via an Apache server on localhost port `8080`

## Screenshots
![](/imgs/1.png)

![](/imgs/2.png)

![](/imgs/3.png)