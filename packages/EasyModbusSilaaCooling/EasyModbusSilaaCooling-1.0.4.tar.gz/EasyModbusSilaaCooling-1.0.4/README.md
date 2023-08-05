# EasyModbusSilaaCooling

This package is modification of the easymodbus package by Stefan Rossmann from "Stefan Rossmann Engineering" and customized to control a Helios KWL EC 170 W by Modbus TCP/IP.

The modfied lines are:

line 741:
length = len(values)*2+7
instead of length = 6

line 791:
length_lsb = length&0xFF;
instead of length_lsb = 0x06;

line 792:
length_msb = (length&0xFF00) >> 8
instead of length_msb = 0x00

If you want to support the original release by Stefan Rossmann, check out his github under [Github-flavored Markdown](https://github.com/rossmann-engineering/EasyModbusTCP.PY) or his website http://easymodbustcp.net/en/ 


