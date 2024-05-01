> HZA Messenger
>
> Hadi Al Hassan, Ahmad Al Maaz, Zeina Merhhad
>
> April 22, 2024

Our project aims to provide a reliable medium for two or more peers to
interchange-ably exchange messages.

1 Project Description

Our application handles the messages exchanged between the two end
systems over UDP. It handles reliability (i.e., handshaking, packet
timeout, a unique twist of AsciiChecksum, and packet reordering).

1.1 Application Function

One peer first initiates the connection, which we may consider as a
client and con-nects to another peer sought as a server. Both peers will
simultaneously exchange messages through creating 2 sockets on both
sides (one for receiving messages and the other for sending messages).

Note that the peer sought as a server will always have two threads
implemented; the first is waiting for a new peer to connect perhaps, and
the second is dedicated to the currently peer that initiated the
connection.

A Three-way handshake is implemented and is ensured to be established
through timeouts.

Messages are fragmented into 1000-byte packets and sent over UDP. The
packets are traced, validated, and later saved to be delivered to the
peer once the message is complete.

Our application also supports file transfer between both peers over TCP;
A dedicated thread is triggered once this feature is requested
separately from the chatting peers.

1.2 Features to be Implemented

>  Modifying the code implementation to utilize selective repeat, using
> a sliding technique.
>
>  Utilizing RSA Encryption to encrypt/decrypt the packets.
>
>  Modifying the code to initialize the connection without the user
> specifying the ports.
>
> 1

2 How To Launch The Application

> 1\. Ensure you have Python 3.10 installed.
>
> 2\. Install the attached ZIP.
>
> 3\. Unzip the ZIP.
>
> 4\. Open your command line.
>
> 5\. CD to the directory containing the files.
>
> 6\. Run the command ”python3 Main.py”.
>
> 7\.  choose between alice and bob,after that choose if you want to initiate connection or no. Due to short time span the handshake will be only visible through the temrinal and not the GUI, if time permits will be added later.
>
>
> 8\. Afterwards the app should launch.

3 How to Use the App

The GUI is very intuitive. You have a text area to enter a message,
press the arrow to send. If you want to send a file, press the file
attachment icon, select the file, and send. Sent messages will be
displayed.

4 Technologies

4.1 Programming Language

Python was a requirement by the instructor, but we would have chosen it
regardless, due to its:

>  Versatility.
>
>  Easiness to read/use/understand.
>
>  Plethora of libraries to use.

4.2 Libraries We Used

>  Socket: necessary to be able to communicate and establish the
> connection.
>
>  Threading: we utilized threads for concurrency (sending and receiving
> simul-taneously).
>
>  Pickle: Pickle allows the user to serialize any built-in Python data
> type and converts them into an array.
>
> 2

5 Challenges Faced

The challenges faced are documented and logged in the report submitted
along with the project.

6 Credits

Credits are well-documented in the report.

7 License

This project is licensed under the [MIT
License](https://opensource.org/licenses/MIT) - feel free to use,
modify, and dis-tribute it, but please provide appropriate credit to the
original authors.

7.1 How to Attribute

When using this project or any parts of it, please include a reference
to the original repository or project, along with a mention of the
original authors. This could be in the form of:

>  A mention in your README file or documentation.
>
>  A comment in the code where you use parts of this project.
>
>  Any other appropriate location where attribution is typically given.

For more information, feel free to contact the authors.

> 3
