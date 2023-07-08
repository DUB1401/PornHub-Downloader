# PornHub-dl by tnt2402

PornHub-dl is a Python tool for downloading PornHub video/playlist.

## Requirements
```bash
Python 3.7 or later
VPN or any anti - Deep Packet Inspection (if your ISP blocks Pornhub) ^-^

```
## Installation


```bash
https://github.com/tnt2402/pornhub_dl.git
cd pornhub_dl
pip install -r requirements.txt
python ./pornhub_dl.py -h
```

## Usage

```python
usage: pornhub_dl.py [-h] [--url URL] [--playlist {most-viewed,best,top-rated,longest}] [--limit LIMIT] [--dir DIR]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             URL of Pornhub video
  --playlist {most-viewed,best,top-rated,longest}
                        Optional ordering of videos (default = best)
  --limit LIMIT         Maximum number of videos
  --dir DIR             Output directory

# download single video from PornHub
pornhub_dl.py --url https://www.pornhub.com/view_video.php?viewkey=ph5b11c7f2ddecc
# download first 30 videos (default = best) from model CarryLight
pornhub_dl.py --url https://www.pornhub.com/model/carrylight --playlist --limit 30
# download all videos (most viewed) from model CarryLight
pornhub_dl.py --url https://www.pornhub.com/model/carrylight --playlist most-viewed
# download first 30 videos (most viewed) from model CarryLight
pornhub_dl.py --url https://www.pornhub.com/model/carrylight --playlist most-viewed --limit 30
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Special thanks
```
YouTube-DL (the world's most powerful tool)

aria2c (a f*ckinn lightweight multi-source command-line download utility)

PyFiglet (simple and beauty)

@ValdikSS for his Deep Packet Inspection circumvention utility (github.com/ValdikSS/GoodbyeDPI)

@mariosemes for his PornHub-downloader (github.com/mariosemes/PornHub-downloader-python)
```

# from tnt2402 with <3
