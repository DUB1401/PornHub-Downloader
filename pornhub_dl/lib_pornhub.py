#!/usr/bin/env python
import sys
import os
import ast
import string
import subprocess
import pyfiglet
import signal
import json
from time import sleep
from tqdm import tqdm
#############


def ascii_banner(text):
    print('\n\n########################################################\n\n\n')
    ascii_banner = pyfiglet.figlet_format(text)
    print(ascii_banner)
################################


# duration = 1000
download_dir = os.getcwd()


def ph_config_dl_dir(dir):
    global download_dir
    if (dir != None):
        download_dir = dir
    print("Output directory: " + download_dir + "\model\\")
    if (os.path.exists(download_dir) != True):
        print('Invalid Directory !')
        sys.exit()
    download_dir = download_dir + "\model\\"
    if (os.path.exists(download_dir) != True):
        os.mkdir(download_dir)


def run_command(command):
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        pbar = tqdm(total=100, unit=" percents")
        state = 0
        current_frag = 0
        total_frag = 1
        result_txt = ''
        while True:
            output = process.stdout.readline().decode("utf-8")
            if "[download] 100" in output:
                result_txt = 'Result: ' + output.split("[download]")[1].strip()

            if output == '' and process.poll() is not None:
                break

            if 'Total fragments' in output:
                total_frag = int(output.split(':')[1].strip())
            if 'FILE:' in output:
                current_frag = int(output.split('.part-Frag')[1].strip())
                current_per = int(current_frag / total_frag * 100)
                pbar.update(current_per - state)
                state = current_per
                sleep(0.00001)
        pbar.update(100 - state)
        pbar.close()
        rc = process.poll()
        if result_txt != '': print(result_txt)
        return rc
    except Exception as e:
        print(e)
        sys.exit(0)

# Main functions


def ph_check_valid_pornhub_url(url):
    if ('pornhub.com' not in url):
        print('Invalid Pornhub URL')
        sys.exit()
    if url.startswith('pornhub.com'):
        url = 'https://www.' + url
    return url


def download_video(url, filename):
    # global duration
    state = 0
    print('[+] Save as: ' + filename + '\n')
    try:
      
        run_command(['.\yt-dlp', '--downloader', 'aria2c', '--downloader-args',
                    'aria2c:-x 8 --log-level=info --file-allocation=none --summary-interval=1', '--no-warnings', '--newline', '-o', filename, url])
      
        print("[$] Video download successfully!")
    except KeyboardInterrupt:
        os.kill(p.pid, signal.CTRL_C_EVENT)
        sys.exit()


def fix_title(s):
    decoded_unicode = ''.join([i if i in string.printable else ' ' for i in s])
    deny_char = ['\\', '/', '.', '?', '*', ':', '!']
    for i in deny_char:
        decoded_unicode = decoded_unicode.replace(i, '')
    return decoded_unicode.strip()


def check_output_dir(model_name):
    global download_dir
    download_dir = download_dir
    if (os.path.exists(download_dir + model_name) != True):
        os.mkdir(download_dir+model_name)


def ph_download_video(url, model_name, filename):

    try:
        check_output_dir(model_name)
        # filename = os.path.join(download_dir, model_name, fix_title(str(video["title"])) + '.' + str(video['ext']))
        download_video(url, filename)
    except:
        print('Cannot download video')


def ph_download_playlist(url, model_name, limit):
    global download_dir
    # global duration
    check_output_dir(model_name)

    if (limit != 0):
        print("[!] Limit: {} videos".format(limit))

    # tmp_playlist download
    print('... Getting playlist information...')
    try:
        playlist_download_command = [".\yt-dlp", "-j",
                                 "--flat-playlist", "--no-check-certificate", url]
        res = subprocess.run(playlist_download_command,
                         capture_output=True, text=True).stdout.split("\n")
    except Exception as e:
        print(e)
        sys.exit(1)
    count = 0

    if res == ['']:
        print("Cannot download playlist information!")
        sys.exit(1)
    print("Playlist has {} videos".format(len(res)))
    
    for i in range(len(res) - 1):
        if (count == limit and limit != 0):
            break
            sys.exit()
        try:
            # print(res[i])
            # video_dict = ast.literal_eval(res[i])
            video_dict = json.loads(res[i])
            url = video_dict['url']
            p = subprocess.Popen(['.\yt-dlp', '--no-warnings', '--dump-json',
                                 '--skip-download', url], stdout=subprocess.PIPE, stderr=None, shell=True)
            output = p.communicate()[0]
            info = json.loads(output.decode('utf-8'))
            # duration = int(info['duration'])
            filename = os.path.join(download_dir, model_name, fix_title(
                str(info["title"])) + '.' + str(info['ext']))
            print("\n\n==========================================\n[+] File #{}: {}".format(
                count, fix_title(str(info["title"])) + '.' + str(info['ext'])))
            ph_download_video(url, model_name, filename)
            count = count + 1
        except KeyboardInterrupt:
            print("Cannot download video")
            sys.exit()


def fix_url(url, type):
    url = ph_check_valid_pornhub_url(url)

    if '/model/' not in url:
        p = subprocess.Popen(['.\yt-dlp', '--no-warnings', '--dump-json',
                             '--skip-download', url], stdout=subprocess.PIPE, stderr=None, shell=True)
        output = p.communicate()[0]
        info = json.loads(output.decode('utf-8'))
        model_name = info['uploader']
    else:
        model_name = url.split('/model/')[1].split('/')[0]

    url = 'www.pornhub.com/model/' + model_name + '/videos'
    if (type == 'most-viewed'):
        url = url + '?o=mv'
    elif (type == 'top-rated'):
        url = url + '?o=tr'
    elif (type == 'longest'):
        url = url + '?o=lg'
    print("[+] Model: " + model_name)
    return (url, model_name)


def ph_get_video(url):
    # global duration
    url = ph_check_valid_pornhub_url(url)

    p = subprocess.Popen(['.\yt-dlp', '--no-warnings', '--dump-json',
                         '--skip-download', url], stdout=subprocess.PIPE, stderr=None, shell=True)
    output = p.communicate()[0]
    info = json.loads(output.decode('utf-8'))
    model_name = info['uploader']
    # duration = int(info['duration'])
    filename = os.path.join(download_dir, model_name, fix_title(
        str(info["title"])) + '.' + str(info['ext']))
    print("[+] Model: " + model_name)
    print("[+] Filename: " + fix_title(str(info["title"])) +
          '.' + str(info['ext']))
    ph_download_video(url, model_name, filename)


def ph_get_playlist(url, type, limit):
    url, model_name = fix_url(url, type)
    ph_download_playlist(url, model_name, limit)
