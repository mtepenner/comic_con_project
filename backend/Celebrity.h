// Celebrity.h
#ifndef CELEBRITY_H
#define CELEBRITY_H

#include <string>

// ==========================================
// Base Class: Celebrity
// ==========================================
class Celebrity {
protected:
    std::string name;

public:
    Celebrity(std::string n) : name(n) {}
    virtual ~Celebrity() {} 

    // Pure virtual functions that enforce structure on subclasses
    virtual void displayInfo() const = 0; 
    virtual std::string getSaveData() const = 0; 
};

#endif
