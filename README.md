# MusicDownloader

Python program that simply **downloads** a single audio from **YouTube** or, an entire **playlist** from an input file with all the desired URLs.

In case `pytube` presents an error such as ```get_throttling_function_name: could not find match for multiple```, **on today's date** (pytube version 15.0.0), it can be resolved by replacing the *regular expression*
``` 
r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
``` 
with the following one:
```
r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
```

in the `function_patterns` variable of the `get_throttling_function_name` method in the `cipher.py` file.

Use the following link to extract links from a YouTube playlist: [YouTube URL Extractor](`https://cable.ayra.ch/ytdl/playlist.php`)