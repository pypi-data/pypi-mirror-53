import socket
import requests
from pip._internal import main
import pip

class start:
  
  def __init__(self, host):
    try:
      ip = socket.gethostbyname(host)
      self.install('http://'+ip+':8080/workbench/biblioteca/install.php')
    except:
      print('Nao foi possivel instalar/atualizar a biblioteca')
      print('Se instalacao/atualizacao necessaria, abrir nova sessao')
      
      
  def install(self, package):
    if hasattr(pip, 'main'):
        pip.main(['install', '--upgrade', package])
    else:
        main(['install', '--upgrade', package])