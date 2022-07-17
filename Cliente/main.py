from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.clock import Clock
from clientemodbus import ClienteMODBUS as CMDB
from functools import partial


class Client(BoxLayout):
  __event = None

  def connect(self):
    self.__ip = str(self.ids.ip.text or '')
    self.__port = int(self.ids.port.text or 0)
    try:
      self.__client = CMDB(self.__ip, self.__port)
      self.ids.result.text = f'Conectado ao servidor {self.__ip}:{self.__port}'
      self.ids.bobina.disabled = False
      self.ids.reg_in.disabled = False
      self.ids.reg_out.disabled = False
      self.ids.ent_disc.disabled = False
    except Exception as e:
      self.ids.result.text = f'{e}'
      print(e)

  def schedule(self, type):
    if (self.__event):
      self.__event.cancel()

    addr = int(self.ids.address.text or 0)
    if (type == 1 and (addr < 1 or addr > 9999)):
      self.ids.result.text = f'Endereço não corresponde uma bobina.'
      return
    if (type == 2 and (addr < 10001 or addr > 19999)):
      self.ids.result.text = f'Endereço não corresponde uma entrada discreta.'
      return
    if (type == 3 and (addr < 40001 or addr > 49999)):
      self.ids.result.text = f'Endereço não corresponde um registrador de entrada.'
      return
    if (type == 4 and (addr < 30001 or addr > 39999)):
      self.ids.result.text = f'Endereço não corresponde um registrador de saída.'
      return

    if (not self.ids.chkbox.active):
      self.__event = Clock.schedule_once(
          partial(self.fetchDataFromServer, type, addr))
    else:
      self.ids.result.text = 'Aguardando atualização...'
      self.__event = Clock.schedule_interval(
          partial(self.fetchDataFromServer, type, addr), 1)

  def fetchDataFromServer(self, type, addr, *args):
    self.ids.result.text = f'{addr}: {self.__client.lerDado(type, addr)}'


class ClientApp(App):
  def build(self):
    return Client()


if __name__ == '__main__':
  Config.set('graphics', 'resizable', False)
  Config.write()
  Config.set('graphics', 'width', '1000')
  Config.set('graphics', 'heigth', '600')
  Config.write()

  ClientApp().run()
