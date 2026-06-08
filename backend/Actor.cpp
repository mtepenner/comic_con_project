#include "Actor.h"

Actor::Actor(std::string n, std::string r) : Celebrity(n), notableRole(r) {}

void Actor::displayInfo() const {} // Suppressed for UI backend

std::string Actor::getSaveData() const {
    return "ACTOR | Name: " + name + " | Role: " + notableRole;
}

ActorNode::ActorNode(Actor a) : data(a), next(nullptr), prev(nullptr) {}

ActorSchedule::ActorSchedule() : head(nullptr), tail(nullptr) {}

ActorSchedule::~ActorSchedule() {
    destroyNodes(head);
}

void ActorSchedule::destroyNodes(ActorNode* current) {
    if (current == nullptr) return;
    ActorNode* nextNode = current->next;
    delete current;
    destroyNodes(nextNode);
}

void ActorSchedule::saveHelper(ActorNode* current, std::ofstream& outFile) const {
    if (current == nullptr) return;
    outFile << current->data.getSaveData() << "\n";
    saveHelper(current->next, outFile);
}

void ActorSchedule::addActor(Actor a) {
    ActorNode* newNode = new ActorNode(a);
    if (head == nullptr) {
        head = tail = newNode;
    } else {
        tail->next = newNode;
        newNode->prev = tail;
        tail = newNode;
    }
}

void ActorSchedule::saveToFile(std::ofstream& outFile) const {
    saveHelper(head, outFile);
}
