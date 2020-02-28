//============================================================================
// Name        : serialTerminal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================


#include <windows.h>

#include <pthread.h>
#include <semaphore.h>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cstdlib>

#include <windows.h>

int kill_kb = 0, kill_tx = 0, kill_rx = 0, kill_proc = 0;
enum outputmode_t {FULL, STAT1};

HANDLE hComm;
outputmode_t output_mode;	//define the output format
std::stringstream  in_str;  //used to dump data from the serial
sem_t wr_sm,rd_sm;

/**********************************************************************/
int get_int_at_spot(std::string s,std::string delimiter, unsigned int spot){

	size_t found = 0;
	int a = 0;
	unsigned int i = 0;
	std::string tempstr;
	if (spot != 0){
		do{
			found = s.find(delimiter,found + 1);
			i++;}
		while (i < spot && found < s.npos);
	}

	if (found != s.npos){
		tempstr = s.substr(found);
		std::stringstream ss(tempstr);
		ss >> a;}


	return a;
}
/**********************************************************************/
typedef unsigned int uint;
typedef std::vector <int> int_vect;
typedef std::vector <int_vect> roi_vect;
/**********************************************************************/
class evt {
	int xmin;
	int xmax;
	int ymin;
	int ymax;


public:
	roi_vect roi;
	evt (uint, uint, uint, uint);
	int roi_size();
	int cols();
	int rows();
	int add_line (std::string line_str);
	void print();

};

int evt::roi_size(){
	return (cols() * rows());}

int evt::cols(){
	return (xmax - xmin + 1);}

int evt::rows(){
	return (ymax - ymin +1 );}

int evt::add_line (std::string line_str){
	int_vect line_vect;
	int i;
	for (i = 0; i < cols(); i++)
	 line_vect.push_back( get_int_at_spot(line_str," ", i) );
	roi.push_back(line_vect);
	return i;
}

void evt::print(){
	roi_vect::iterator r_it;
	int_vect::iterator c_it;

	for (r_it = roi.begin(); r_it != roi.end(); ++r_it){
		for (c_it = r_it->begin(); c_it != r_it->end(); ++c_it)
			std::cout << *c_it << " ";
		std::cout << std::endl;
	}
}

evt::evt (uint Xmin, uint Xmax, uint Ymin, uint Ymax){
	xmin = Xmin; xmax = Xmax; ymin = Ymin; ymax = Ymax;
}
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
  SetupComm(hComm,10000,1000);
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
	std::cout << "'quit' to quit" << std::endl;
	std::cout << "'h', 'help' for this list" << std::endl;
}

/**********************************************************************/
void *rxthread_job (void* par){
	std::string Templine; //Temporary character used for reading
	char TempChar;
	DWORD NoBytesRead = 0;
	int lpar = *(int*)par;


	Templine.clear();
	std::cout << "rx Thread Started " << lpar << std::endl;

	while  (hComm != INVALID_HANDLE_VALUE && !kill_rx){

		   ReadFile( hComm,           //Handle of the Serial port
		             &TempChar,       //Temporary character
		             sizeof(TempChar),//Size of TempChar
		             &NoBytesRead,    //Number of bytes read
		             NULL);

		   if(NoBytesRead){
			   Templine += TempChar;
			   if (TempChar=='\n'){
			   sem_wait(&wr_sm);
			   in_str << Templine;
			   sem_post(&rd_sm);}
		   }


		   }

	return NULL;
}


/**********************************************************************/
void *procthread_job (void* par){
	std::string templine;
	int xmin = 0, xmax = 0, ymin = 0, ymax = 0;
	int ROI_rows, ROI_cols;
	char ch;



	while (!kill_proc){
		/********************/
		sem_wait(&rd_sm);
		getline (in_str, templine);
		in_str.clear();
		sem_post(&wr_sm);
		/*********************************************/
		if (templine.find("ROI") != templine.npos){
			//ROI coordinates section
			std::cout << "found ROI" << std::endl;
			xmin =  get_int_at_spot(templine," ", 6); xmax = get_int_at_spot(templine," ", 7);
			ymin =  get_int_at_spot(templine," ", 8); ymax = get_int_at_spot(templine," ", 9);

			/********************/
			sem_wait(&rd_sm);
			getline (in_str, templine);
			in_str.clear();
			sem_post(&wr_sm);
			/********************/
			if (templine.find("event data:") != templine.npos){
			//event data
			evt event(xmin,xmax,ymin,ymax);
			std::cout << "found event with " << event.rows() << " rows and " ;
			std::cout << event.cols() << " cols -> "<< event.roi_size() <<std::endl;
			do{
				/********************/
				sem_wait(&rd_sm);
				getline (in_str, templine);
				in_str.clear();
				sem_post(&wr_sm);
				/********************/

				if(templine.find("end of event") == templine.npos)
					event.add_line(templine);
				}
			while (templine.find("end of event") == templine.npos && !kill_proc);

			}
		}
		/*********************************************/
		else
			std::cout << "Unrecognized TAG: " << templine << std::endl;



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

		if (kbstr == "quit"){
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
	sem_init(&wr_sm, 0, 1);
	sem_init(&rd_sm, 0, 0);

	serial_open(port, baudrate);

	pthread_create( &rx_thread, NULL, rxthread_job, (void*)&par);

	pthread_create( &tx_thread, NULL, txthread_job, (void*)&par);

	pthread_create( &kb_thread, NULL, kbthread_job, (void*)&par);

	pthread_create( &proc_thread, NULL, procthread_job, (void*)&par);

	pthread_join(kb_thread, (void**)&retval);

	serial_close();

	return 0;
}
