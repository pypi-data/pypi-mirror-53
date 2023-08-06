# distutils: language = c++
# cython: language_level = 3
#encoding = utf-8
DEF_CHIP_ID_FLASH   =   0x3C
DEF_CHIP_ID_METRO   =   0xC3
DEF_MODEL_8X8       =   0x08
#Адреса регистров модуля:   
REG_FLAGS_0         =   0x00
REG_BITS_0          =   0x01
REG_FLAGS_1         =   0x02
REG_BITS_1          =   0x03
REG_MODEL           =   0x04
REG_VERSION         =   0x05
REG_ADDRESS         =   0x06
REG_CHIP_ID         =   0x07
REG_FREQUENCY       =   0x08
REG_BRIGHTNESS      =   0x09
REG_8X8_DATA        =   0x10
REG_8X8_SAVE_AS     =   0x19
REG_8X8_SYMBOL_INPUT=   0x1A
REG_8X8_TEXT_INPUT  =   0x1B
REG_8X8_STEP_LEN    =   0x1C
REG_8X8_TIME_STEP   =   0x1E
REG_8X8_TIME_PAUSE  =   0x1F
REG_8X8_TIME_START  =   0x20
REG_8X8_TIME_STOP   =   0x21
REG_8X8_FUNCTIONS   =   0x22
#Функций анимации ряби:     
X8_EMPTY_RIPPLES    =   100 
X8_RIPPLES          =   101 
X8_FILLED_RIPPLES   =   102 
#Функций анимации сверху-вниз
X8_EMPTY_DOWN       =   104 
X8_DOWN             =   105 
X8_FILLED_DOWN      =   106 
#Функций анимации снизу-вверх
X8_EMPTY_TOP        =   108 
X8_TOP              =   109 
X8_FILLED_TOP       =   110 
#Виды памяти для хранения изо
X8_IMG_RAM          =   0   
X8_IMG_ROM          =   1   
#Виды поддерживаемых кодирово
X8_TXT_CP866        =   0   
X8_TXT_UTF8         =   1   
X8_TXT_WIN1251      =   2   
#Выключение автоинициализации
NO_BEGIN = 1

from iarduino_I2C_Matrix_8x8 cimport iarduino_I2C_Matrix_8x8
from time import sleep

cdef class pyiArduinoI2Cmatrix:
    cdef iarduino_I2C_Matrix_8x8 c_matrix

    def __cinit__(self, address=None, auto=None):
        if address is not None:
            self.c_matrix = iarduino_I2C_Matrix_8x8(address)
            if auto is None:
                sleep(.5)
                self.c_matrix.begin()
        else:
            self.c_matrix = iarduino_I2C_Matrix_8x8()
            if auto is None:
                sleep(.5)
                self.c_matrix.begin()

    def begin(self):
        return self.c_matrix.begin()

    def changeAddress(self, unsigned char newAddr):
        return self.c_matrix.changeAddress(newAddr)

    def reset(self):
        return self.c_matrix.reset()

    def getAddress(self):
        return self.c_matrix.getAddress()

    def getVersion(self):
        return self.c_matrix.getVersion()

    def getCoding(self):
        return self.c_matrix.getCoding()

    def setCoding(self, name):
        self.c_matrix.setCoding(name)

    def codingDetect(self, letter_p):
        if isinstance(letter_p, str) and len(letter_p) is 1:
            self.c_matrix.codingDetect(str.encode(letter_p))
        else:
            print("ошибка: функция принимет только букву 'п'")

    def clrScr(self, ani = None):
        if ani is not None:
            self.c_matrix.clrScr(ani)
        else:
            self.c_matrix.clrScr(0)

    def fillScr(self, ani = None):
        if ani is not None:
            self.c_matrix.fillScr(ani)
        else:
            self.c_matrix.fillScr(0)

    def invScr(self):
        self.c_matrix.invScr()

    def drawImage(self, array, ani = None):
        if isinstance(array, list):
            b = bytearray(array)
            if ani is None:
                self.c_matrix.drawImage(b, 0, 0)
            elif isinstance(ani, int):
                self.c_matrix.drawImage(b, ani, 0)
            else:
                print("неверен второй аргумент функции: "
                      +" должен быть целым числом\n"
                      + "вызов функции:\n"
                      + ".drawImage(СПИСОК, ЦЕЛОЕ ЧИСЛО)")
        else:
            print("неверен первый аргумент функции: "
                  + " должен быть списком\n"
                  + "вызов функции:\n"
                  + ".drawImage(СПИСОК, [ЦЕЛОЕ ЧИСЛО])")

    def getImage(self):
        image = [0,0,0,0,0,0,0,0]
        b = bytearray(image)
        self.c_matrix.getImage(b)
        image = list(b)
        return image

    def print(self, mes, ani = None):
        """
        Функция вывода числа или строки на матрицу.
        ОБЪЕКТ.print(СТРОКА или ЦЕЛОЕ ЧИСЛО, [ЦЕЛОЕ ЧИСЛО])
        Параметры:
            параметр1: число или строка для вывода
            параметр2: целое число - номер анимации для вывода:
                Анимация ряби:
                X8_EMPTY_RIPPLES
                X8_RIPPLES
                X8_FILLED_RIPPLES
                Функций анимация сверху-вниз
                X8_EMPTY_DOWN
                X8_DOWN
                X8_FILLED_DOWN
                Функций анимация снизу-вверх
                X8_EMPTY_TOP
                X8_TOP
                X8_FILLED_TOP
        Пример:
            m = pyiArduinoI2Cmatrix()
            m.print("A", X8_RIPPLES)
        """
        if isinstance(mes, str):
            b = bytearray(mes, "utf-8")
            if ani is None:
                self.c_matrix.print(b, 0)
            elif isinstance(ani, int):
                self.c_matrix.print(b, ani)
            else:
                print("неверен второй аргумент функции: "
                      +" должен быть целым числом\n"
                      + "вызов функции:\n"
                      + ".print(СТРОКА или ЦЕЛОЕ ЧИСЛО, ЦЕЛОЕ ЧИСЛО)")
        elif isinstance(mes, int):
            if ani is None:
                self.c_matrix.printNum(mes, 0)
            elif isinstance(ani, int):
                self.c_matrix.printNum(mes, ani)
            else:
                print("неверен второй аргумент функции: "
                      +" должен быть целым числом\n"
                      + "вызов функции:\n"
                      + ".print(СТРОКА или ЦЕЛОЕ ЧИСЛО, ЦЕЛОЕ ЧИСЛО)")
        elif isinstance(mes, float):
            if ani is None:
                self.c_matrix.printNum(int(mes), 0)
            elif isinstance(ani, int):
                self.c_matrix.printNum(int(mes), ani)
            else:
                print("неверен второй аргумент функции: "
                      +" должен быть целым числом\n"
                      + "вызов функции:\n"
                      + ".print(СТРОКА или ЦЕЛОЕ ЧИСЛО, ЦЕЛОЕ ЧИСЛО)")
        else:
            print("неверен первый аргумент функции: "
                  + " должен быть строкой или целым числом\n"
                  + "вызов функции:\n"
                  + ".print(СТРОКА или ЦЕЛОЕ ЧИСЛО, [ЦЕЛОЕ ЧИСЛО])")

    def autoScroll(self, speed, interval = None):
        if interval is None:
            self.c_matrix.autoScroll(speed, 0)
        else:
            self.c_matrix.autoScroll(speed, interval)

    def scrollPos(self, position):
        self.c_matrix.scrollPos(position)

    def scrollDir(self, direction):
        self.c_matrix.scrollDir(direction)

    def scrollMod(self, mode):
        self.c_matrix.scrollMod(mode)

    def scrollStep(self):
        self.c_matrix.scrollStep()

    def setTimeIdleFirst(self, time):
        self.c_matrix.setTimeIdleFirst(time)

    def setTimeIdleLast(self, time):
        self.c_matrix.setTimeIdleLast(time)

    def getScroolLen(self):
        return self.c_matrix.getScroolLen()

    def getScroolWidth(self):
        return self.c_matrix.getScroolWidth()

    def angle(self, angle):
        self.c_matrix.angle(angle)

    def fps(self, fps):
        self.c_matrix.fps(fps)

    def bright(self, brightness):
        self.c_matrix.bright(brightness)

    def changeChar(self, sym):
       self.c_matrix.changeChar(sym) 

    def setCharWidth(self, width):
       self.c_matrix.setCharWidth(width) 

    def setCharInterval(self, interval):
       self.c_matrix.setCharInterval(interval) 

    def setCharIndent(self, indent):
       self.c_matrix.setCharIndent(indent)

    def getCharWidth(self):
        return self.c_matrix.getCharWidth()

    def getCharInterval(self):
        return self.c_matrix.getCharInterval()

    def getCharIndent(self):
        return self.c_matrix.getCharIndent()
