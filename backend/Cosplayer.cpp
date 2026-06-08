#include "Cosplayer.h"

Cosplayer::Cosplayer(std::string n, std::string c) : Celebrity(n), character(c) {}

void Cosplayer::displayInfo() const {} // Suppressed for UI backend

std::string Cosplayer::getSaveData() const {
    return "COSPLAYER | Name: " + name + " | Character: " + character;
}

CosplayerNode::CosplayerNode(Cosplayer c) : data(c), next(nullptr) {}

CosplayerParade::CosplayerParade() : head(nullptr) {}

CosplayerParade::~CosplayerParade() {
    if (head == nullptr) return;
    destroyNodes(head->next);
    delete head;
}

void CosplayerParade::destroyNodes(CosplayerNode* current) {
    if (current == head) return;
    CosplayerNode* nextNode = current->next;
    delete current;
    destroyNodes(nextNode);
}

CosplayerNode* CosplayerParade::findTail(CosplayerNode* current) {
    if (current->next == head) return current;
    return findTail(current->next);
}

void CosplayerParade::saveHelper(CosplayerNode* current, std::ofstream& outFile) const {
    outFile << current->data.getSaveData() << "\n";
    if (current->next == head) return;
    saveHelper(current->next, outFile);
}

void CosplayerParade::addCosplayer(Cosplayer c) {
    CosplayerNode* newNode = new CosplayerNode(c);
    if (head == nullptr) {
        head = newNode;
        newNode->next = head;
    } else {
        CosplayerNode* tail = findTail(head);
        tail->next = newNode;
        newNode->next = head;
    }
}

void CosplayerParade::saveToFile(std::ofstream& outFile) const {
    if (head == nullptr) return;
    saveHelper(head, outFile);
}
