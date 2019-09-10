# scone-hello

This hello world project provides demonstrates how to run C++ applications capable to be run in iExec environment
Currently it's possible to run only python processes, that is why your app should be converted into form of shared library
and called from python via ctypes. All fork, spawn, exec methods do not work in iexechub/python-scone image from 8/5/2019

# Publishing application for testing on kovan chain
1. Edit deploy.py and provide your password to avoid entering it each time on line 27 add to the end: 'default="yourpassword",'
2. Either start in fresh folder, or remove existing iexec json files, you can avoid it and use script with --force option: 
    ```
    rm *.json
    ```
3. After you have built image, you can call python script deploy.py to publish your app to the chain. You can use it in two modes:
    a. if you have iexec cli setup on same system just run

    ```
    python3 deployment/deploy.py --image_url "dockerhubtag" --tee [--name "your-app-name"]  [--price 5]
    ```
    b. if you are running iexec cli on different host, than you can use remote mode

    ```
    python3 deployment/deploy.py --mode remote --image_url "sdxkeeper/gva-inference-app:scone-simple-0.0.20" --tee --mrenclave "40b336410d34f107cXXXXXXX161adf435d5b8d84dd4bb2cb1936de44e8b4a2|8c24db06044d73XXXXXf84feb65c83d6|cd12bcf962f626006a1d30620f205d1f6XXXXXX15a67d1f45d3b20398f55d23" [--name "your-app-name"] [--price 5]
    ```
