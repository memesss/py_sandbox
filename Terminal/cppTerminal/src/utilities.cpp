/*
 * utilities.cpp
 *
 *  Created on: 29 feb 2020
 *      Author: xpol
 */
#include "utilities.h"

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


