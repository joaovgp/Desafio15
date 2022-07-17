from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import random


class ServidorMODBUS():
  """
  Classe Servidor MODBUS
  """

  def __init__(self, host_ip, port):
    """
    Construtor
    """

    self._server = ModbusServer(host=host_ip, port=port, no_block=True)

  def run(self):
    """
     Execução do servidor
    """
    self._server.start()
    print("Servidor em execução")
    while True:
      self._server

      self._server.data_bank.set_coils(
          1000, [bool(random.getrandbits(1))])  # bobina on/off
      self._server.data_bank.set_discrete_inputs(
          10001, [bool(random.getrandbits(1))])  # entrada discreta on/off
      self._server.data_bank.set_input_registers(
          30001, [random.randrange(0, 65536)])  # registradores de entrada
      self._server.data_bank.set_holding_registers(
          40001, [random.randrange(0, 65536)])  # registradores de saída

      print('======================')
      print("Tabela MODBUS")
      print(
          f'Coil \r\n R1000: {self._server.data_bank.get_coils(1000)} \r\n\nDiscrete Input \r\n R10001: {self._server.data_bank.get_discrete_inputs(10001)} \r\n\nInput Register \r\n R30001: {self._server.data_bank.get_input_registers(30001)} \r\n\nHolding Register \r\n R40001: {self._server.data_bank.get_holding_registers(40001)}')
      sleep(1)
