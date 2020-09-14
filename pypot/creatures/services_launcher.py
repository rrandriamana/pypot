#!/usr/bin/env python



import os
import sys
import time
import random
import logging
import argparse
import webbrowser
import subprocess

from contextlib import closing
from argparse import RawTextHelpFormatter

from pypot.server.snap import find_local_ip
from pypot.creatures import installed_poppy_creatures
from pypot.utils import flushed_print as print

from multiprocessing import Process
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler


def start_poppy_with_services(args):
    params = poppy_params_from_args(args)

    for i in range(5):
        try:
            print('Attempt {} to start the robot...'.format(i + 1))
            return installed_poppy_creatures[args.creature](**params)

        except Exception as e:
            # In case of failure,
            # Give the robot some time to statup, reboot...
            time.sleep(random.random())
            print(e)
    else:
        print('Could not start up the robot...')
        sys.exit(1)


def poppy_params_from_args(args):
    params = {
        'use_snap': args.snap,
        'snap_port': args.snap_port,
        'use_http': args.http,
        'http_port': args.http_port,
        'use_remote': args.remote,
        'use_ws': args.ws,
        'ws_port': args.ws_port,
    }

    if args.verbose:
        params['snap_quiet'] = False
        params['http_quiet'] = False
        params['ws_quiet'] = False

    if args.vrep:
        params['simulator'] = 'vrep'
    elif args.poppy_simu:
        params['simulator'] = 'poppy-simu'
    elif args.dummy:
        params['simulator'] = 'dummy'

    if args.disable_camera:
        params['camera'] = 'dummy'

    return params


def main():
    parser = argparse.ArgumentParser(
        description=('Poppy services launcher. Use it to quickly instantiate a ' +
                     'poppy creature with Scratch, an http server, or a remote robot.'),
        epilog="""
Examples:
* poppy-services --snap poppy-torso
* poppy-services --snap --vrep poppy-humanoid""",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('creature', type=str,
                        help='poppy creature name',
                        action='store', nargs='?',
                        choices=list(installed_poppy_creatures.keys()))
    parser.add_argument('--dummy',
                        help='use a simulated dummy robot',
                        action='store_true')
    parser.add_argument('--vrep',
                        help='use a V-REP simulated Poppy Creature',
                        action='store_true')
    parser.add_argument('--poppy-simu',
                        help='start a simulated dummy robot and the HTTP API to connect to the viewer on simu.poppy-project.org',
                        action='store_true')
    parser.add_argument('--snap',
                        help='start a Scratch robot server',
                        action='store_true')
    parser.add_argument('--snap-port',
                        help='port used by the Scratch server',
                        default=6969, type=int)
    parser.add_argument('-nb', '--no-browser',
                        help='avoid automatic start of Scratch in web browser',
                        action='store_true')
    parser.add_argument('--http',
                        help='start a http robot server',
                        action='store_true')
    parser.add_argument('--http-port',
                        help='port of HttpRobotServer, used for poppy-simu',
                        default=8080, type=int)
    parser.add_argument('--remote',
                        help='start a remote robot server',
                        action='store_true')
    parser.add_argument('--ws',
                        help='start the websocket server',
                        action='store_true')
    parser.add_argument('--ws-port',
                        help='port of Websocket Server',
                        default=9009, type=int)
    parser.add_argument('--disable-camera',
                        help='Start the robot without the camera.',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='start services with verbose mode. There is 3 debug levels, add as "v" as debug level you want',
                        action='count')
    parser.add_argument('-f', '--log-file',
                        help='Log filename',
                        action='store')

    nb_creatures = len(installed_poppy_creatures.keys())
    if nb_creatures == 0:
        print('No installed poppy creature were found!')
        print('You should first install the python package '
              'corresponding to your robot or check your python environment.')
        sys.exit(1)

    args = parser.parse_args()

    # If no creature are specified and only one is installed
    # We use it as default.
    if args.creature is None:
        if nb_creatures > 1:
            parser.print_help()
            sys.exit(1)

        args.creature = list(installed_poppy_creatures.keys())[0]
        print('No creature specified, use {}'.format(args.creature))

    if args.log_file:
        fh = logging.FileHandler(args.log_file)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logging.getLogger('').addHandler(fh)

    if args.verbose:
        args.snap_quiet = False
        args.http_quiet = False
        args.ws_quiet = False

        if args.verbose == 1:
            lvl = logging.WARNING
        elif args.verbose == 2:
            lvl = logging.INFO
        elif args.verbose > 2:
            lvl = logging.DEBUG

        if args.log_file is not None:
            ch = logging.FileHandler(args.log_file)
        else:
            ch = logging.StreamHandler()

        ch.setLevel(lvl)
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s')
        ch.setFormatter(formatter)
        logging.getLogger('').addHandler(ch)

    if not any([args.snap, args.http, args.remote, args.poppy_simu, args.ws, args.dummy]):
        print('No service specified! See --help for details.')
        sys.exit(1)

    static_server_started = False
    if args.snap and not args.no_browser:     
        snap_static_port = 8888
        snap_static_server = HTTPServer(("0.0.0.0", snap_static_port), SimpleHTTPRequestHandler)

        from pypot.vpl.snap import download_snap_interactively
        static_app = download_snap_interactively()
        if static_app is None:
            print("The static server was not started because the VPL app has not been downloaded")
        else:
        os.chdir(static_app)
        snap_static_server_process = Process(target=snap_static_server.serve_forever, args=())
        static_server_started = True
        snap_static_server_process.start()
        os.chir('schratch-gui')
        subprocess.Popen(['./node_modules/webpack-dev-server/bin/webpack-dev-server.js', '--host 0.0.0.0  --disable-host-check'])

        #snap_url = 'http://127.0.0.1:{}/snap.html'.format(snap_static_port)
        #block_url = 'http://{}:{}/snap-blocks.xml'.format(
        #    find_local_ip(), args.snap_port)
        url = 'http://127.0.0.1:8601/' #'{}#open:{}'.format(snap_url, block_url)

    with closing(start_poppy_with_services(args)):

        msg=''

        if args.dummy or args.poppy_simu:
            msg+= 'Simulated robot created! He is running on: ip={}'.format(find_local_ip())
        else:
            msg+= 'Robot instantiated! He is running on: ip={},'.format(find_local_ip())
            if args.disable_camera: msg+= ' without camera access.'
            else: msg+= ' with camera access.'

        if args.vrep: msg+= ' With V-REP link.'

        if args.snap or args.ws or args.http or args.poppy_simu:
            msg+= '\nServer started on:'
            if args.http or args.poppy_simu: msg+= ' http_port={},'.format(args.http_port)
            if args.snap: msg+= ' Snap_port={},'.format(args.snap_port)
            if args.ws: msg+= ' ws_port={},'.format(args.ws_port)
            msg= msg[0:-1]+'.'

        print(msg)

        sys.stdout.flush()

        if static_server_started:
            for browser_name in ['chromium-browser', 'chromium', 'google-chrome',
                                'chrome', 'safari', 'midori', None]:
                try:
                    browser = webbrowser.get(browser_name)
                    browser.open(url, new=0, autoraise=True)
                    break
                except Exception:
                    pass

        # Just run4ever (until Ctrl-c...)
        try:
            while(True):
                time.sleep(1000)
        except KeyboardInterrupt:
            print("Bye bye!")
            if static_server_started:
                snap_static_server_process.terminate()
                snap_static_server_process.join()


if __name__ == '__main__':
    main()
