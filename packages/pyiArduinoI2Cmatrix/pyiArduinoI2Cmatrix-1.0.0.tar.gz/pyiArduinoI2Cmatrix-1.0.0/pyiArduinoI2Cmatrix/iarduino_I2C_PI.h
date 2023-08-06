#ifndef iarduino_I2C_h                  // Разрешаем включить данный код в скетч, только если он не был включён ранее
#define iarduino_I2C_h                  // Запрещаем повторное включение данного кода в скетч
#define delay(A) usleep(A*1000)         // Определяем макрос для подмены delay() на usleep() для Raspberry (необходима подгруженная библиотека unistd.h)
#define lowByte(w) ((uint8_t) ((w) & 0xff))
#define highByte(w) ((uint8_t) ((w) >> 8))
#include <unistd.h>                     // Подключаем библиотеку unistd, для получения доступа к POSIX API
#include <fcntl.h>                      // Подключаем библиотеку доступа к файлам
#include <sys/ioctl.h>                  // Подключаем библиотеку контроля входов/выходов
#include <linux/i2c-dev.h>              // Подключаем библиотеку для работы с шиной i2c
#include <stdint.h>                     // Подключаем библиотеку с макросами целочисленных типов
                                        //
class iarduino_I2C_BASE{                                                                        //  Определяем полиморфный класс
        public:                                                                                 //  Доступные методы и функции:
//  ОСНОВНЫЕ ФУНКЦИИ:                                                                           //
                virtual void begin(uint32_t){};                                                 //  Аргументы: скорость в кГц.
                virtual uint8_t readByte(uint8_t, uint8_t){return 0;};                          //  Аргументы: адрес_модуля, адрес_регистра. (адрес регистра указывает модулю, данные какого регистра требуется отправить мастеру)
                virtual bool writeByte(uint8_t, uint8_t, uint8_t) {return 0;};                  //  Аргументы: адрес_модуля, адрес_регистра, байт_данных. (адрес регистра указывает модулю, в какой регистр требуется сохранить данные)
                virtual uint8_t readByte(uint8_t){return 0;};                                   //  Аргументы: адрес_модуля  (функция отличается тем, что она не отправляет модулю адрес регистра)
                virtual bool writeByte(uint8_t, uint8_t){return 0;};                            //  Аргументы: адрес_модуля, байт_данных. (функция отличается тем, что она не отправляет модулю адрес регистра)
                virtual bool readBytes(uint8_t, uint8_t, uint8_t*, uint8_t)  {return 0;};       //  Аргументы: адрес_модуля, адрес_первого_регистра, указатель_на_массив, количество_байт. (адрес первого регистра указывает модулю, с какого регистра требуется начать передачу данных мастеру)
                virtual bool writeBytes(uint8_t, uint8_t, uint8_t*, uint8_t){return 0;};        //  Аргументы: адрес_модуля, адрес_первого_регистра, указатель_на_массив, количество_байт. (адрес первого регистра указывает модулю, начиная с какого регистра требуется сохранять данные)
                virtual bool readBytes(uint8_t, uint8_t*, uint8_t)  {return 0;};                //  Аргументы: адрес_модуля, указатель_на_массив, количество_байт. (функция отличается тем, что она не отправляет модулю адрес первого регистра, а начинает цикл чтения сразу после отправки адреса модуля.)
                virtual bool writeBytes(uint8_t, uint8_t*, uint8_t){return 0;};                 //  Аргументы: адрес_модуля, указатель_на_массив, количество_байт. (функция отличается тем, что после отправки адреса модуля она сразу начинает цикл отправки данных, без передачи адреса первого регистра.)
//  ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:                                                                     //
                virtual bool checkAddress(uint8_t){return 0;};                                  //  Аргументы: адрес_модуля.
                virtual void changeBus(char*){};                                                //
};                                                                                              //
                                                                                                //
class iarduino_I2C: public iarduino_I2C_BASE{                                                   //  Определяем производный класс
        public:                                                                                 //
                                                                                                //
        /**  ОСНОВНЫЕ ФУНКЦИИ: **/                                                              //
                                                                                                //
//      Функция подготовки шины I2C:                                                            //
                void begin(uint32_t speed)                                                      //
                {  //  Аргумент: скорость шины в кГц (не используется, задать скорость можно только в файле /boot/config.txt с последующей перезагрузкой, что находится за пределами данной библеотеки).
                        if((file_i2c = open(filename, O_RDWR))<0) return;                       //  Открываем файл шины i2c. Если модель Raspberry ревизии 2.0 (выпущена после 2012 года) - i2c-1, если ревизия 1.0 - i2c-0. Узнать номер шины можно вызвав ls /dev в консоли. 
                }

//      Функция чтения одного байта из регистра модуля:
                uint8_t readByte(uint8_t adr, uint8_t reg)
                {  //  аргументы: адрес_модуля, адрес_регистра
                        uint8_t i=0; readBytes(adr, reg, &i, 1);
                        return i;
                }

//      Функция чтения одного байта из модуля:
                uint8_t readByte(uint8_t adr)
                {
                        uint8_t i=0; readBytes(adr, &i, 1);
                        return i;
                }

//      Функция записи одного байта в регистр модуля:
                bool writeByte(uint8_t adr, uint8_t reg, uint8_t data)
                {
                        return writeBytes(adr, reg, &data, 1);
                }

//      Функция записи одного байта в модуль:
                bool writeByte(uint8_t adr, uint8_t data)
                {
                        return writeBytes(adr, &data, 1);
                }

//      Функция пакетного чтения нескольких байт данных из регистров модуля:
/*              bool readBytes(uint8_t addr, uint8_t reg, uint8_t *data, uint8_t sum)
                {   // аргументы: адрес_модуля, адрес_первого_регистра, указатель_на_массив, количество_байт
                        if (ioctl(file_i2c, I2C_SLAVE, addr) < 0) return false;
                        else if ((write(file_i2c, &reg, 1) != 1) && usleep(1000)) return false;
                        else if (read(file_i2c, data, sum) != sum) return false;
                        else return true;
                }
*/
                bool readBytes(uint8_t addr, uint8_t reg, uint8_t *data, uint8_t sum)
                {  // аргументы: адрес_модуля, адрес_первого_регистра, указатель_на_массив, количество_байт
                        if (ioctl(file_i2c, I2C_SLAVE, addr) < 0) return false;
                        else if ((write(file_i2c, &reg, 1) != 1)) return false;
                        usleep(10);
                        if (read(file_i2c, data, sum) != sum) return false;
                        else return true;
                }

//      Функция пакетного чтения нескольких байт данных из модуля:
                bool readBytes(uint8_t addr, uint8_t *data, uint8_t sum)
                {  // аргументы: адрес_модуля, указатель_на_массив, количество_байт
                        if (ioctl(file_i2c, I2C_SLAVE, addr) < 0) return false;
                        else if (read(file_i2c, data, sum) != sum) return false;
                        else return true;
                }

//      Функция пакетной записи нескольких байт данных в регистр модуля:
                bool writeBytes(uint8_t addr, uint8_t reg, uint8_t *data, uint8_t sum)
                {  // аргументы: адрес_модуля, адрес_первого_регистра, указатель_на_массив, количество_байт
                        uint8_t length = sum+1;
                        uint8_t data_with_reg[length];
                        for (int i=1; i < length; i++) {
                                        data_with_reg[i] = data[i-1];
                        }
                        data_with_reg[0] = reg;
                        if (ioctl(file_i2c, I2C_SLAVE, addr) < 0)
                                return false;
                        else if (write(file_i2c, data_with_reg,
                                       length) != length) return false;
                        else return true;
                }

//      Функция пакетной записи нескольких байт данных в модуль:
                bool writeBytes(uint8_t addr, uint8_t *data, uint8_t sum)
                {  // аргументы: адрес_модуля, указатель_на_массив, количество_байт
                        if (ioctl(file_i2c, I2C_SLAVE, addr) < 0) return false;
                        else if (write(file_i2c, data, sum) !=sum) return false;
                        else return true;
                }

        /**     ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ: **/

//              Функция проверки наличия ведомого по его адресу:
                bool checkAddress(uint8_t addr)
                {  // аргументы: адрес_регистра, байт_данных
                        if (ioctl(file_i2c, I2C_SLAVE, addr) < 0) return false;
                        else return true;
                }

                void changeBus(char* bus){
                        this->filename = bus;
                }
        private:                                                                                                                                                //
                char *filename = (char*)"/dev/i2c-1";
                int file_i2c;
};                                                                                                                                                                      //
#endif                                                                                                                                                          //
