//============================================================================
// Name        : serialTerminal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <pthread.h>
#include <semaphore.h>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <iomanip>

#include "SComm.h"
#include "event.h"
#include <ctime>
#include "utilities.h"

int kill_kb = 0, kill_tx = 0, kill_rx = 0, kill_proc = 0;
enum outputmode_t {FULL, STAT1};

SComm *Serial;
outputmode_t output_mode;	//define the output format
std::stringstream  in_str;  //used to dump data from the serial
sem_t wr_sm,rd_sm;
unsigned int event_counter;
unsigned int pha_outliers_counter;
float pha_avg_avg;
/**********************************************************************/
void print_help(){
	std::cout << "'quit' to quit" << std::endl;
	std::cout << "'h', 'help' for this list" << std::endl;
}

/**********************************************************************/
void *rxthread_job (void* par){
	std::string Templine; //Temporary character used for reading
	char TempChar;
	int lpar = *(int*)par;


	Templine.clear();
	std::cout << "rx Thread Started " << lpar << std::endl;

	while  (!kill_rx){

		TempChar = Serial->getc();

		Templine += TempChar;
		if (TempChar=='\n'){
			   sem_wait(&wr_sm);
			   in_str << Templine;
			   Templine.clear();
			   sem_post(&rd_sm);}
		 }

	return NULL;
}

/**********************************************************************/
void popline(std::string &templine){
	sem_wait(&rd_sm);
	getline (in_str, templine);
	in_str.clear();
	sem_post(&wr_sm);
	}

int check_string(std::string templine, std::string test_str){
	size_t shorter = templine.size();
	if (shorter > test_str.size()) shorter = test_str.size();
    return templine.compare(0,shorter,test_str);
}
/********************************************************************/
void *collectorthread_job (void* par){
	std::string templine;
	int xmin = 0, xmax = 0, ymin = 0, ymax = 0;

	while (!kill_proc){
		/********************/
		popline(templine);
		/*********************************************/
		if (templine.find("ROI") != templine.npos){
			//ROI coordinates section

			xmin =  get_int_at_spot(templine," ", 6); xmax = get_int_at_spot(templine," ", 7);
			ymin =  get_int_at_spot(templine," ", 8); ymax = get_int_at_spot(templine," ", 9);

			/********************/
			popline(templine);
			/********************/
			if (check_string(templine,"event data:")  == 0){

			//event
			event evt(xmin,xmax,ymin,ymax);

			do{
				/********************/
				popline(templine);
				/********************/

				if(check_string(templine,"end of event") != 0)
					evt.add_line(templine);
				}
			while (check_string(templine,"end of event") != 0 && !kill_proc);
			event_counter ++;
			float pha = evt.get_pha(0);
			float pha_avg = evt.get_avg_pha(0);

			pha_avg_avg = (pha_avg_avg * ((float)event_counter - 1.0) + pha_avg) / (float) event_counter;

					if (pha_avg > 2.507){
						pha_outliers_counter ++;
						 std::cout << "event pha > " << pha << "avg >"
						 << pha_avg <<" @ time " << ctime(&evt.timestamp) << std::endl;
						 evt.print();
						}
					/*if (evt.roi_size()>396){
						std::cout << "roi size " << evt.roi_size() << " @ time "
						<< ctime(&evt.timestamp) << std::endl;
					}*/

				}

			}
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
void print_stats(){
	std :: cout << "event counter-> " << event_counter << std::endl;
	std :: cout << "pha_outliers_counter-> " << pha_outliers_counter
			<<" "<< 100.0 * float(pha_outliers_counter) / float (event_counter) << "%"
			<<std::endl;
	std :: cout << "pha_avg_avg-> " << pha_avg_avg << std::endl;
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
			print_stats();
			}
		else if (kbstr == "stat"){
			print_stats();
		}
		if (kbstr == "h" || kbstr =="help")
			print_help();
		}
	return NULL;
}


int main(int argc, char** argv) {

	pthread_t rx_thread, tx_thread, kb_thread, collector_thread;
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
	event_counter = 0;
	pha_outliers_counter = 0;
	pha_avg_avg = 0.0;
	sem_init(&wr_sm, 0, 1);
	sem_init(&rd_sm, 0, 0);

	Serial = new SComm(port, baudrate);

	pthread_create( &rx_thread, NULL, rxthread_job, (void*)&par);

	pthread_create( &tx_thread, NULL, txthread_job, (void*)&par);

	pthread_create( &kb_thread, NULL, kbthread_job, (void*)&par);

	pthread_create( &collector_thread, NULL, collectorthread_job, (void*)&par);

	pthread_join(kb_thread, (void**)&retval);
	delete(Serial);

	return 0;
}
