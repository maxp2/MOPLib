#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

void generate_Samte_SEAM_SEAF()
{
    std::vector<std::string> rows, columns;
    
    rows.push_back("A");
    rows.push_back("B");
    rows.push_back("C");
    rows.push_back("D");
    rows.push_back("E");
    rows.push_back("F");
    rows.push_back("G");
    rows.push_back("H");
    
    std::ofstream pin_file;
    pin_file.open("Samtec_SEAM_SEAF.txt");
    
    pin_file << "Object Kind\tX1\tY1\tOrientation\tName\tShow Name\tPin Designator\tShow Designator\tRow\tColumn\tIndex" << std::endl;
    
    unsigned int index = 0;
    
    for (auto r = rows.begin(); r < rows.end(); r++)
    {
        for (unsigned int c = 1; c <= 50; c++)
        {
            pin_file << "Pin\t";
            pin_file << "0mil\t";
            pin_file << std::to_string(100*c) << "mil\t";
            pin_file << "180 Degrees\t";
            pin_file << "pin\t";
            pin_file << "false\t";
            pin_file << *r << std::to_string(c) << "\t";
            pin_file << "true\t";
            pin_file << *r << "\t";
            pin_file << c << "\t";
            pin_file << std::to_string(index) << "\t";
            pin_file << "\n";
            
            index++;
        }
    }
    
    pin_file.close();
}
