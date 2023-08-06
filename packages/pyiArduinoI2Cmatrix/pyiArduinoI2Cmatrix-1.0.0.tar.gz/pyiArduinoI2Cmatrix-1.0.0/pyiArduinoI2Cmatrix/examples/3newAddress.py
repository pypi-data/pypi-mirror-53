# Данный пример меняет адрес модуля на указанный в newAddress.  #
                                        #
newAddress = 0x09                       # Назначаемый модулю адрес.
                                        #
from pyiArduinoI2Cmatrix import *       # Подключаем библиотеку для работы с LED матрицей 8x8.
disp = pyiArduinoI2Cmatrix()            # Объявляем объект disp для работы с функциями pyiArduinoI2Cmatrix.
                                        # Если при объявлении объекта указать адрес, например, disp(0x0B), то пример будет работать с тем модулем, адрес которого был указан.
if disp.begin() is True:                # Инициируем работу с LED матрицей 8x8.
    print("На шине I2C найден "         #
          "модуль с адресом "           #
          + hex(disp.getAddress())      # Выводим текущий адрес модуля.
          + " который является"         #
          " LED матрицей 8x8")          #
    if disp.changeAddress(              #
            newAddress) is True:        # Меняем адрес модуля на newAddress.
                                        # 
        print("Адрес модуля изменён на "#
              + hex(disp.getAddress())) # Выводим текущий адрес модуля.
    else:                               #
        print("Адрес модуля "           #
              "изменить не удалось!")   #
else:                                   # 
    print("Модуль LED матрица"          #
          " 8x8 не найден!")            #
