// Данный пример выводит изображения myImage_1 и myImage_2.      //
#include "../iarduino_I2C_Matrix_8x8.h"                             // Подключаем библиотеку для работы с LED матрицей 8x8.
//#include <cstdint>
#include <cstdlib>
#include <iostream>
typedef unsigned char byte;
                                                                 // Создаём изображение "смайлик".
byte myImage_1[8] = { 0b00111100,                                //                        ####
                      0b01000010, /* Посмотрите, изображение */  //                       #    #
                      0b10100101, /* можно увидеть прямо в   */  //                      # #  # #
                      0b10000001, /* коде!!!                 */  //                      #      #
                      0b10100101,                                //                      # #  # #
                      0b10011001,                                //                      #  ##  #
                      0b01000010,                                //                       #    #
                      0b00111100 };                              //                        ####
                                                                 // Создаём изображение "телевизор".
byte myImage_2[8] = { 0b01000100,                                //                       #   #  
                      0b00101000,                                //                        # #   
                      0b00010000,                                //                         #    
                      0b11111111,                                //                      ########
                      0b10000011,                                //                      #     ##
                      0b10000011,                                //                      #     ##
                      0b10000011,                                //                      #     ##
                      0b11111111 };                              //                      ########
iarduino_I2C_Matrix_8x8 disp;                              // Объявляем объект disp для работы с LED матрицей 8x8, указывая её адрес на шине I2C.

void loop(void);
                                                                 //
int main(int argc, char** argv){                                                    //
    if(argc > 1) {

        std::cout << atoi(argv[1]) << '\n';
        disp = atoi(argv[1]);
        delay(500);                                                  // Ждём завершение переходных процессов связанных с подачей питания.
        disp.begin();                                                // Инициируем работу с LED матрицей 8x8.
        for (;;) {
            loop();
        }
    } else {
        std::cout << "not enough arguments\n";
    }
}                                                                //
                                                                 //
void loop(){                                                     //
    disp.drawImage(myImage_1); delay(2000);                      // Выводим на дисплей изображение массива myImage_1 и ждём пару секунд.
    disp.drawImage(myImage_2); delay(2000);                      // Выводим на дисплей изображение массива myImage_2 и ждём пару секунд.
}                                                                //
