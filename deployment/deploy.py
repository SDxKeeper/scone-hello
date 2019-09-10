import os
import json
import argparse
import docker
import subprocess
from colorama import Fore
from requests import exceptions
import getpass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='automate deployment of new image into scone.')
    parser.add_argument('--image_url', type=str, dest='image_url', required=True,
                        help='docker image url')
    parser.add_argument('--name', type=str, dest='name', default='test-app',
                        help='application name')

    parser.add_argument('--mode', type=str, choices=['local', 'remote'], default='local',
                        help='Script can operate in local and remote modes: \
                            in local mode image will be used to extract mrenclave, \
                            in remote mode mrenclave should be provided as argument')
    parser.add_argument('--mrenclave', type=str, dest='mrenclave',
                        help='mrenclave of the image')
    parser.add_argument('--price', type=int, dest='appprice', default=0,
                        help='price for the app, default free')
    parser.add_argument('--tee', action='store_true', default=False,
                        help='Use tee tag in app order')
    parser.add_argument('--password', type=str, dest='password',
                        help='wallet password')
    parser.add_argument('--force', action='store_true', default=False,
                        help='overwrite existing iexec files')

    args = parser.parse_args()

    if not args.force and (os.path.exists("iexec.json") or os.path.exists("chain.json") or os.path.exists("orders.json") or os.path.exists("deployed.json")):
        print("iexec.json already exists, exiting to prevent overwrite!")
        exit()

    wallet_password = None
    if args.password is None:
        # ask for password
        wallet_password = getpass.getpass(prompt='Wallet password:')
    else:
        wallet_password = args.password

    dclient = docker.from_env()
    image_sha256 = ''
    mrenclave = None
    if args.mode == 'remote':
        if args.mrenclave is None:
            print(Fore.RED + "Please provide MREnclave for remote operation mode (image is not available to extract it automatically)")
            exit()

        if args.tee and args.mrenclave is None:
            print("tee apps require mrenclave to be set")
            exit()

        mrenclave = args.mrenclave
        try:
            registry_data = dclient.images.get_registry_data(args.image_url)
            image_sha256 = registry_data.id.split(":")[1]
        except docker.errors.APIError as error:
            print(Fore.RED + "Could not retrieve registry information for image %s Error: %s" %(args.image_url, error))
            exit()


    elif args.mode == 'local':
        image = dclient.images.get(args.image_url)
        image_sha256 = image.id.split(":")[1]
        result_fp = dclient.containers.run(args.image_url, entrypoint='cat', command='/conf/fingerprint.txt')
        #print(result_fp)
        mrenclave = result_fp.decode("utf-8")

    print(Fore.RED + "Supplied image sha256 hash is " + Fore.GREEN + "%s" % image_sha256)
    print(Fore.RED + "MREnclave: " + Fore.GREEN + "%s" % mrenclave)

    completed = subprocess.run(["iexec","init", "--skip-wallet"])
    if completed.returncode != 0:
        print("call to iexec failed")
        exit(completed.returncode)

    completed = subprocess.run(["iexec","app", "init"])
    if completed.returncode != 0:
        print("call to iexec failed")
        exit(completed.returncode)

    iexec = json.loads(open("iexec.json").read())
    #print(iexec)

    iexec["app"]["name"] = args.name
    iexec["app"]["multiaddr"] = "registry.hub.docker.com/" + args.image_url
    iexec["app"]["checksum"] = "0x" + image_sha256

    iexec["app"]["mrenclave"] = args.mrenclave if args.mrenclave is not None else ""

    print(json.dumps(iexec["app"], sort_keys=True, indent=4))
    json.dump(iexec, open("iexec.json", "w"))

    completed = subprocess.run(["iexec","app", "deploy", "--password", wallet_password])
    if completed.returncode != 0:
        print("call to iexec failed")
        exit(completed.returncode)

    completed = subprocess.run(["iexec","order", "init", "--app"])
    if completed.returncode != 0:
        print("call to iexec failed")
        exit(completed.returncode)

    iexec = json.loads(open("iexec.json").read())

    iexec["order"]["apporder"]["tag"] = "0x0000000000000000000000000000000000000000000000000000000000000001" if args.tee else "0x0000000000000000000000000000000000000000000000000000000000000000"
    
    iexec["order"]["apporder"]["appprice"] = args.appprice
    print(json.dumps(iexec["order"]["apporder"], sort_keys=True, indent=4))

    json.dump(iexec, open("iexec.json", "w"))

    completed = subprocess.run(["iexec","order", "sign", "--app",  "--password", wallet_password])
    if completed.returncode != 0:
        print("call to iexec failed")
        exit(completed.returncode)

    completed = subprocess.run(["iexec","order", "publish", "--app", "--force", "--password", wallet_password])
    if completed.returncode != 0:
        print("call to iexec failed")
        exit(completed.returncode)

