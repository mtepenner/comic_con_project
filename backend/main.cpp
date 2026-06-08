// main.cpp
#include <iostream>
#include <string>
#include <limits>
#include <fstream>

// Import our modularized headers
#include "Artist.h"
#include "Actor.h"
#include "Cosplayer.h"

using namespace std;

// ==========================================
// Recursive Controller
// ==========================================
void clearInputBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

void runMenu(ArtistManager& artistAlley, ActorSchedule& mainStage, CosplayerParade& conventionFloor) {
    int choice = 0;
    string name, detail;
    int number;

    cout << "READY" << endl; // Signal to python that we are ready for input
    
    if (!(cin >> choice)) {
        return; // Base Case: Exit on pipe close
    }
    clearInputBuffer(); 

    if (choice == 1) {
        getline(cin, name);
        getline(cin, detail);
        cin >> number;
        artistAlley.addArtist(Artist(name, detail, number));
    } 
    else if (choice == 2) {
        getline(cin, name);
        getline(cin, detail);
        mainStage.addActor(Actor(name, detail));
    } 
    else if (choice == 3) {
        getline(cin, name);
        getline(cin, detail);
        conventionFloor.addCosplayer(Cosplayer(name, detail));
    } 
    else if (choice == 4) {
        // UI triggers this to force an update to the text file without exiting
        ofstream outFile("comicon_data.txt");
        if (outFile.is_open()) {
            outFile << "=== OFFICIAL COMIC-CON REGISTRY ===" << endl;
            artistAlley.saveToFile(outFile);
            mainStage.saveToFile(outFile);
            conventionFloor.saveToFile(outFile);
            outFile.close();
            cout << "SAVED" << endl;
        }
    } 
    else if (choice == 5) {
        return; // Base Case: Exit the recursive loop completely
    } 

    runMenu(artistAlley, mainStage, conventionFloor); // Recursive execution
}

int main() {
    ArtistManager artistAlley;
    ActorSchedule mainStage;
    CosplayerParade conventionFloor;
    
    runMenu(artistAlley, mainStage, conventionFloor);
    
    return 0;
}
