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

typedef unsigned int uint;
typedef std::vector <int> int_vect;
typedef std::vector <int_vect> roi_vect;


class event {
		int xmin;
		int xmax;
		int ymin;
		int ymax;

	public:
		roi_vect roi;
		event (uint, uint, uint, uint);
		int roi_size();
		int cols();
		int rows();
		int add_line (std::string line_str);
		void print();
		virtual ~event();

};

#endif /* EVENT_H_ */
