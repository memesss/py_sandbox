/*
 * event.cpp
 *
 *  Created on: 29 feb 2020
 *      Author: xpol
 */

#include "event.h"


int event::roi_size(){
	return (cols() * rows());}

int  event::cols(){
	return (xmax - xmin + 1);}

int event::rows(){
	return (ymax - ymin +1 );}

int event::add_line (std::string line_str){
	int_vect line_vect;
	int i;
	for (i = 0; i < cols(); i++)
	 line_vect.push_back( get_int_at_spot(line_str," ", i) );

	roi.push_back(line_vect);
	return i;
}

void event::print(){
	roi_vect::iterator r_it;
	int_vect::iterator c_it;

	std::cout << "ROI " << xmin <<" "<< xmax <<" "<< ymin << " " << ymax << std::endl;

	for (r_it = roi.begin(); r_it != roi.end(); ++r_it){
		for (c_it = r_it->begin(); c_it != r_it->end(); ++c_it)
			std::cout << std::setfill(' ') << std::setw(4) << *c_it << " ";
		std::cout << std::endl;
	}
}
/****************************************************/
float event::get_pha(float threshold){
	float acc = 0.0;
	roi_vect::iterator r_it;
	int_vect::iterator c_it;

	for (r_it = roi.begin(); r_it != roi.end(); ++r_it){

		for (c_it = r_it->begin(); c_it != r_it->end(); ++c_it)

			if (*c_it >= threshold)
					acc  += *c_it;
	}
	return acc;
}
/****************************************************/
float event::get_avg_pha(float threshold){
	float acc = 0.0;
	roi_vect::iterator r_it;
	int_vect::iterator c_it;

	for (r_it = roi.begin(); r_it != roi.end(); ++r_it){

		for (c_it = r_it->begin(); c_it != r_it->end(); ++c_it)

			if (*c_it >= threshold)
					acc  += *c_it;
	}
	return acc/roi_size();
}
/****************************************************/
event::event (uint Xmin, uint Xmax, uint Ymin, uint Ymax){
	xmin = Xmin; xmax = Xmax; ymin = Ymin; ymax = Ymax;
	time(&timestamp);
}

event::~event() {
	// TODO Auto-generated destructor stub
}

