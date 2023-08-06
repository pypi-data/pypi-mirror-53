cdef extern from "iarduino_I2C_Matrix_8x8.cpp":
    pass

cdef extern from "itoa.cpp":
    pass

cdef extern from "dtostrf.cpp":
    pass

cdef extern from "WString.cpp":
    pass

cdef extern from "iarduino_I2C_Matrix_8x8.h":
    cdef cppclass iarduino_I2C_Matrix_8x8:
        iarduino_I2C_Matrix_8x8() except +
        iarduino_I2C_Matrix_8x8(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()
        unsigned char getCoding()
        void setCoding(unsigned char)
        void codingDetect(char*)
        void clrScr(unsigned char)
        void fillScr(unsigned char)
        void invScr()
        void drawImage(unsigned char*, unsigned char, unsigned char)
        void getImage(unsigned char*)
        void print(char*, unsigned char)
        void printNum "print"(short, unsigned char)
#        void print(str, unsigned char)
        void autoScroll(unsigned char, unsigned short)
        void scrollPos(unsigned short)
        void scrollDir(bint)
        void scrollMod(bint)
        void scrollStep()
        void setTimeIdleFirst(unsigned short)
        void setTimeIdleLast(unsigned short)    
        unsigned short getScroolLen() 
        unsigned short getScroolWidth()   
        void angle(unsigned short)          
        void fps(unsigned char)             
        void bright(unsigned char) 
        void changeChar(unsigned char) 
        void setCharWidth(unsigned char) 
        unsigned char getCharWidth()  
        void setCharInterval(unsigned char)    
        unsigned char getCharInterval()    
        void setCharIndent(unsigned char)  
        unsigned char getCharIndent()  

cdef extern from "iarduino_I2C_PI.h":
    cdef cppclass iarduino_I2C:
        void changeBus(unsigned char)

