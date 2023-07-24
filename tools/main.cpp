//g++ -o ./outputs/main ./main.cpp ./pin_array_generator.cpp &> ./outputs/build.log

#include <iostream>

void generate_Samte_SEAM_SEAF();

int main()
{
    std::cout << "Start of program" << std::endl;
    std::cout << "Build Timestamp : " << __DATE__ << " " << __TIME__ << std::endl;
    
    generate_Samte_SEAM_SEAF();
    
    std::cout << "End of program" << std::endl;
    
    return 0;
}
