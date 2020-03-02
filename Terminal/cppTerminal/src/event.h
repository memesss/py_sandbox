/*
 * event.h
 *
 *  Created on: 29 feb 2020
 *      Author: xpol
 */

#ifndef EVENT_H_
#define EVENT_H_

#include <vector>
#include <string>
#include <iomanip>
#include "utilities.h"
#include <ctime>

typedef unsigned int uint;
typedef std::vector <float> int_vect;
typedef std::vector <int_vect> roi_vect;


class event {
		int xmin;
		int xmax;
		int ymin;
		int ymax;


	public:
		time_t timestamp;
		roi_vect roi;
		event (uint, uint, uint, uint);
		int roi_size();
		int cols();
		int rows();
		int add_line (std::string line_str);
		float get_pha(float threshold);
		void print();
		virtual ~event();

};

#endif /* EVENT_H_ */
