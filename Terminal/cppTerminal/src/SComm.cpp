/*
 * SComm.cpp
 *
 *  Created on: 29 feb 2020
 *      Author: xpol
 */

#include "SComm.h"


/****************************************/
SComm::SComm(std::string port, int baudrate) {

	// TODO Auto-generated constructor stub
	/**********************************************************************/

		std::string port_string = "\\\\.\\" + port;

		hComm = CreateFile( port_string.c_str(),                //port name
		                      GENERIC_READ | GENERIC_WRITE, //Read/Write
		                      0,                            // No Sharing
		                      NULL,                         // No Security
		                      OPEN_EXISTING,// Open existing port only
		                      0,            // Non Overlapped I/O
							  NULL);        // Null for Comm Devices

	  if (hComm == INVALID_HANDLE_VALUE)
	      std::cout << "Error in opening serial port " << port_string << std::endl;
	  else
	  {
	  std::cout << "opening serial port " << port_string << " successful" << std::endl;
	  DCB dcbSerialParams = { 0 }; // Initializing DCB structure
	  dcbSerialParams.DCBlength = sizeof(dcbSerialParams);

	  GetCommState(hComm, &dcbSerialParams);
	  dcbSerialParams.BaudRate = baudrate;  // Setting BaudRate
	  dcbSerialParams.ByteSize = 8;         // Setting ByteSize = 8
	  dcbSerialParams.StopBits = ONESTOPBIT;// Setting StopBits = 1
	  dcbSerialParams.Parity   = NOPARITY;  // Setting Parity = None

	  SetCommState(hComm, &dcbSerialParams);}
	}
/****************************************/
SComm::~SComm() {
	// TODO Auto-generated destructor stub
	close();
}
/****************************************/
char SComm::getc(){
	char TempChar;
	int NoBytesRead;

	do{
	   ReadFile( hComm,           //Handle of the Serial port
	             &TempChar,       //Temporary character
	             sizeof(TempChar),//Size of TempChar
	             &NoBytesRead,    //Number of bytes read
				 NULL);
		}
	 while (NoBytesRead==0 && hComm != INVALID_HANDLE_VALUE);
	 return TempChar;
}
/****************************************/
int SComm::close(){
	if (hComm != INVALID_HANDLE_VALUE)
		CloseHandle(hComm);//Closing the Serial Port
	return 1;
}
/****************************************/
int SComm::tx (){
		return 1;
}
