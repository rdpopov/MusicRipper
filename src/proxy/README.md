# Responsibilities
* Scrape proxies from a website and store them.
* Do requests with said proxies and return the result.
* 60 second timeout on a request and retry.
* If a proxy is productive keep it around for a next request.
* If scrape new ones if the count in the queue becomes bellow a 100.
