/*
 * SComm.h
 *
 *  Created on: 29 feb 2020
 *      Author: xpol
 */

#ifndef SCOMM_H_
#define SCOMM_H_

#include <windows.h>
#include <iostream>
#include <string>


class SComm {
	HANDLE hComm;
public:
	SComm(std::string port, int baudrate);
	char getc();
	int close();
	int tx();
	virtual ~SComm();
};

#endif /* SCOMM_H_ */
