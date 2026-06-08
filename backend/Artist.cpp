#include "Artist.h"

Artist::Artist(std::string n, std::string s, int b) : Celebrity(n), style(s), boothNumber(b) {}

void Artist::displayInfo() const {} // Suppressed for UI backend

std::string Artist::getSaveData() const {
    return "ARTIST | Name: " + name + " | Style: " + style + " | Booth: " + std::to_string(boothNumber);
}

void ArtistManager::saveHelper(size_t index, std::ofstream& outFile) const {
    if (index >= artists.size()) return;
    outFile << artists[index].getSaveData() << "\n";
    saveHelper(index + 1, outFile);
}

void ArtistManager::addArtist(Artist a) {
    artists.push_back(a);
}

void ArtistManager::saveToFile(std::ofstream& outFile) const {
    saveHelper(0, outFile);
}
