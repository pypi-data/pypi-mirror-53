# podfeed
`podfeed` is a python3 package that will read an RSS feed for a podcast and provide episode-level utilties for download or playlist creation.

## Installation
```
$ pip install podfeed
```

## Example Usage
```python
from podfeed import parseFeed

# Collect episodes published after May 1st, 2018 
episodes = parseFeed("https://www.npr.org/rss/podcast.php?id=510289", 1525132800)

# Write each episode to a file
for episode in episodes:
  episode.writeFile("./{0}_{1}.{2}".format(
    episode.getTitle(), episode.getDate(), episode.getExt()))
```

## Documentation
[podfeed Documentation](https://mmazzocchi.github.io/podfeed/)

## Logging
`podfeed` uses the built-in python [logging module](https://docs.python.org/3/library/logging.html), using loggers with the top-level name `podfeed`.
