🚀 Features
Client
Modern UI: Built using customtkinter with support for dynamic theme changes.

Animated Side Menu: Smooth sliding sidebar animation to hide or show settings.

Adaptive Layout: Dynamically resizes UI elements based on the window's dimensions.

Asynchronous Networking: Uses Python's threading library to receive messages in the background without freezing the GUI.

Message Buffer Parsing: Safe socket data streaming that cleanly parses messages ending with a newline (\n).

Server
Multi-threaded Architecture: Handles multiple client connections concurrently using individual threads.

Efficient Broadcasting: Forwards incoming messages to all connected users except the sender.

Robust Error Handling: Cleanly drops disconnected clients and manages active connection states.

🛠️ Project Structure & Protocol
The application communicates via simple TCP sockets. Messages are structured using a specific string format:

Plaintext
TYPE@USERNAME@MESSAGE\n
TYPE: The type of communication (e.g., TEXT).

USERNAME: The display name of the message sender.

MESSAGE: The actual text content.

\n: Delimiter used to signify the end of a complete packet.

⚙️ Getting Started
Prerequisites
Python 3.7 or higher

customtkinter library

Install the UI dependency using pip:

Bash
pip install customtkinter
Installation & Running
1. Start the Server
Run the server script on your host machine or cloud instance. By default, it listens on port 8080.

Bash
python server.py
2. Configure the Client
In the client script, update the socket connection configuration inside the __init__ constructor to match your server's host IP/domain and port:

Python
self.sock.connect(('YOUR_SERVER_IP_OR_NGROK_URL', PORT))
(Note: The default code is configured to route through an ngrok TCP tunnel).

3. Launch the Client
Run the client application:

Bash
python client.py
🖥️ UI Configuration Guide
Side Menu Toggle (👉🏻 / 👈🏻): Expands or collapses the menu profile options.

Theme Dropdown: Allows you to change the application's appearance:

Africa: Switches to Dark Mode.

Europa: Switches to Light Mode.

Text Input: Type your message at the bottom and hit ☝🏻 to send it instantly.
