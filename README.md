# 🚀 Comic-Con Terminal Management System

## Description
The Comic-Con Terminal Management System is a full-stack, cyber-themed desktop application designed to manage convention scheduling, guest itineraries, and secure billing. It bridges a high-performance C++ backend for efficient data structure management with a sleek, terminal-inspired Python Tkinter graphical user interface using Inter-Process Communication (IPC).

## 📑 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features
* **Cyberpunk UI:** A visually striking, terminal-inspired GUI built with Tkinter featuring custom color schemes.
* **Role-Based Access Control:** Distinct operational modes for `ROOT` (Admin) and `USER` (Guest) accounts.
* **Secure Authentication:** User credentials are encrypted using salted PBKDF2-HMAC-SHA256 hashing.
* **Efficient Data Management:** The C++ backend utilizes advanced data structures including Doubly Linked Lists (Actor Schedules), Circular Linked Lists (Cosplayer Parades), and Vectors (Artist Alley).
* **Cross-Language IPC:** Seamless data pipelining between the Python frontend and C++ executable via `stdin`/`stdout`.
* **Dynamic Ledger Routing:** Integrated financial routing configuration and invoice generation for guests.

## 🛠️ Technologies Used
* **Backend:** C++11
* **Frontend:** Python 3, Tkinter
* **Data Storage:** JSON (Authentication/Banking), TXT (Convention Data)
* **Build System:** GNU Make

## ⚙️ Installation

### Prerequisites
* **Python 3.x** installed on your system.
* **g++ compiler** (supporting C++11 standard).
* **Make** build utility.

### Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/mtepenner/comic_con_project.git
   cd comic-con-project

```

2. **Configure Executable Path (Mac/Linux Users):**
By default, the Python frontend looks for a Windows `.exe` file. If you are on Mac or Linux, open `frontend/config.py` and update the execution path:
```python
# Change from "backend/backend.exe" to:
CPP_EXECUTABLE = "backend/backend" 

```


3. **Build and Run:**
Use the provided Makefile to compile the C++ backend and launch the Python GUI simultaneously:
```bash
make all

```



## 💻 Usage

* **Authentication:** Upon launch, allocate a new account or log in. Choose the `ROOT` (Admin) privilege level to manage the convention or `USER` (Guest) to browse. You can also "Bypass as Guest" for quick access.
* **Admin Portal:** Use the mainframe to inject new Artists, Actors, and Cosplayers into the databanks. You can also configure the financial routing ledger.
* **Guest Portal:** Browse the official Comic-Con registry, multi-select events to build your itinerary, and execute a secure checkout using simulated credits (SECURE_NET or CRYPTO_LEDGER).

## 📂 Project Structure

```text
comic_con_project/
├── Makefile                # Build and run configurations
├── backend/                # C++ source code for data handling
│   ├── Actor.h / .cpp      # Doubly Linked List implementation
│   ├── Artist.h / .cpp     # Vector implementation
│   ├── Cosplayer.h / .cpp  # Circular Linked List implementation
│   ├── Celebrity.h / .cpp  # Base class
│   └── main.cpp            # C++ Entry Point & IPC Controller
└── frontend/               # Python/Tkinter GUI application
    ├── admin_ui.py         # Administrator portal
    ├── auth_ui.py          # Login and registry UI
    ├── config.py           # Theme and path configurations
    ├── guest_ui.py         # Guest itinerary and billing UI
    ├── main.py             # Python Entry Point
    └── managers.py         # Authentication and Ledger handling

```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/yourusername/comic-con-project/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
