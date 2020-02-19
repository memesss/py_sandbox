//============================================================================
// Name        : serialTerminal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================


#include <windows.h>

#include <pthread.h>
#include <iostream>
#include <string>
#include <sstream>

#include <windows.h>

int kill_kb = 0, kill_tx = 0, kill_rx = 0, kill_proc = 0;
enum outputmode_t {FULL, STAT1};

HANDLE hComm;
outputmode_t output_mode;	//define the output format
std::stringstream  in_str;  //used to dump data from the serial
/**********************************************************************/
int serial_open (std::string port, int baudrate){

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

return 1;
}
/**********************************************************************/

int serial_close(){
	if (hComm != INVALID_HANDLE_VALUE)
		CloseHandle(hComm);//Closing the Serial Port
return 1;
}

int serial_tx(){
	return 1;
}


/**********************************************************************/
void print_help(){
	std::cout << "'QUIT' to quit" << std::endl;
	std::cout << "'h', 'help' for this list" << std::endl;
}

/**********************************************************************/
void *rxthread_job (void* par){
	char TempChar; //Temporary character used for reading
	DWORD NoBytesRead = 0;
	int lpar = *(int*)par;

	std::cout << "rx Thread Started " << lpar << std::endl;

	while  (hComm != INVALID_HANDLE_VALUE && !kill_rx){

		   ReadFile( hComm,           //Handle of the Serial port
		             &TempChar,       //Temporary character
		             sizeof(TempChar),//Size of TempChar
		             &NoBytesRead,    //Number of bytes read
		             NULL);
		   if(NoBytesRead)
		    in_str << TempChar;}

	return NULL;
}
/**********************************************************************/
void *procthread_job (void* par){
	std::string templine = "";
	int Xmin, Xmax, Ymin, Ymax;
	int ROI_rows, ROI_cols;
	while (!kill_proc){

		getline(in_str, templine);


		if (templine.find("ROI") != std::string::npos){
			//ROI coordinates section
			std::stringstream tempstream(templine);
			 tempstream >> Xmin; tempstream >> Xmax; tempstream >> Ymin; tempstream >> Ymax;
			 std::cout << "Xmin, Xmax,Ymin,Ymax" << Xmin << Xmax << Ymin << Ymax << std::endl;
			}

		else if (templine.find("event data") != std::string::npos){
			//event data
			ROI_rows = 0; ROI_cols = 0;

			while (templine.find("event end") == std::string::npos && !kill_proc){
				getline(in_str, templine);
				ROI_rows++;}

			std::cout << "found event with " << ROI_rows << std::endl;
			}

		else{
			std::cout << "Unrecognized TAG: " << templine;
			}

		templine.clear();

		}

	return NULL;
}
/**********************************************************************/
void *txthread_job (void* par){
	int lpar = *(int*)par;
	std::cout << "Tx Thread Started " << lpar << std::endl;
	std::string rxstr = "";
	return NULL;
}
/**********************************************************************/
void *kbthread_job (void* par){
	int lpar = *(int*)par;

	std::string kbstr = "";
	std::cout << "Kb Thread Started " << lpar << std::endl;

	while (!kill_kb) {
		std::cout << "Type (h=help): ";
		getline(std::cin, kbstr);

		std::cout << "You Typed: " << kbstr << std::endl;

		if (kbstr == "QUIT"){
			kill_kb = 1;
			kill_rx = 1;
			kill_tx = 1;
			}
		if (kbstr == "h" || kbstr =="help")
			print_help();
		}
	return NULL;
}


int main(int argc, char** argv) {

	pthread_t rx_thread, tx_thread, kb_thread, proc_thread;
	std::string port;
	int baudrate;
	int par = 5;
	int retval;
	/**********************/
	if (argc > 1)
		port = argv[1];
	else
		port = "COM1";

	if (argc >2)
		baudrate = atoi (argv[2]);
	else
		baudrate = 115200;
	/*********************/
	serial_open(port, baudrate);

	pthread_create( &rx_thread, NULL, rxthread_job, (void*)&par);

	pthread_create( &tx_thread, NULL, txthread_job, (void*)&par);

	pthread_create( &kb_thread, NULL, kbthread_job, (void*)&par);

	pthread_create( &proc_thread, NULL, procthread_job, (void*)&par);


	pthread_join(kb_thread, (void**)&retval);

	serial_close();

	return 0;
}
