import click
from ain.workerMgr import Worker
import ain.constants as constants
import requests

def checkVersion():
  MESSAGE = {
    "jsonrcp": "2.0",
    "method": "ain_checkCliVersion",
    "params": {
      "version": constants.VERSION
    },
    "id": 1
  }

  try:
    response = requests.get(constants.TRACKER_ADDR, data=MESSAGE)
    if (response.json()['result'] == 0): return True
    else: return False
  except Exception as e:
    print("[-] tracker server error")
    print(e)
    return False


@click.group()
@click.option('--type/--no-type', default=False)
def call(type):
  pass

@call.command()
@click.argument("command", type=click.Choice(['start', 'stop', 'status', 'log', 'init', 'version']))
@click.option('--name', default="", help="Ain Worker name")
@click.option('--max-instance-count ', default="", help="maximum number of Instances")
@click.option('--price', default="", help="ain/h")
@click.option('--mnemonic', default="", help="mnemonic")
@click.option('--description', default="empty", help="description")
@click.option('--server-ip', default="empty", help="Cloud Server IP")
@click.option('--gpu', default="false", help="gpu")
def worker(command, name, max_instance_count, price, mnemonic, description, server_ip, gpu):

  optionRun = {
    'NAME': name,
    'LIMIT_COUNT': max_instance_count,
    'MNEMONIC': mnemonic,
    'PRICE': price,
    'DESCRIPTION': description,
    'GPU': gpu,
    'SERVER_IP': server_ip
  }

  if checkVersion() == False:
    print('[!] you have to input "sudo pip3 install --upgrade ain-worker"')
    exit(1)
        
  w = Worker()  
  if (command == "start"):
    w.start(optionRun)
  elif (command == "stop"):
    w.stop()
  elif (command == "status"):
    w.status()
  elif (command == "log"):
    w.log()
  elif (command == "init"):
    w.init()
  elif (command == "version"):
    print(constants.VERSION)
    
if __name__ == '__main__':
  call()
