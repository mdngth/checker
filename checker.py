import os
import psutil
from datetime import datetime

import sys

g_log_file = 'checker.log'
g_dt = datetime.now()
g_log_size = 30 # Mb

for p in psutil.process_iter():
  #if p.pid != 0 and p.pid != 4:
  #
  if p.name() == 'TOTALCMD64.EXE':
    print(str(p.pid) + ' || ' + str(p.name()) + ' || ' + str(p.exe()) + ' || ' + str(p.cmdline()))

## --------------------------------------------------------------------------------------------------------

def logger(p_type, p_tag, p_message):
  # проверим перед этим размер лог файла, и если тот превышает размер - переключим
  if round(os.stat(g_log_file).st_size/1024/1024) > g_log_size:
    os.rename(g_log_file, g_log_file + '.old.' + g_dt.strftime("%d%m%Y%H%M%S"))

  # добавим в лог
  with open(g_log_file, 'a') as f:
    f.write(g_dt.strftime("%d.%m.%Y %H:%M:%S") + ' [' + p_type + '] ' + p_tag + ': ' + p_message + '\n')

def find_proc(p_name):
  # проходимся по всем процессам и ищем нужный
  for p in psutil.process_iter():
    if p.name() ==  p_name:
      try:
        v_pid = p.pid
        v_exe = p.exe()
        v_cmdline = p.cmdline()
      except:
        logger('ERROR', 'FIND_PROC', str(sys.exc_info()[0]) + ': ' + str(sys.exc_info()[1]))
        # возвращаем -2, т.к. произошло что-то непредвиденное на этапе получения информации о процессе
        return -2, ''
      #
      return v_pid, v_exe, v_cmdline
  # если ничего не нашли, возвращаем -1
  return -1, ''

## --------------------------------------------------------------------------------------------------------

a, b = find_proc('TOTALCMD64')