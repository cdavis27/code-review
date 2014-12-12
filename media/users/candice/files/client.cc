#include "client.h"

bool debug = false;

Client::Client() {
    // setup variables
    buflen_ = 1024;
    buf_ = new char[buflen_+1];
}

Client::~Client() {
}

void Client::run() {
    create();
    echo();
}

void Client::create() {



}

void Client::close_socket() {
}

string getMessage() {
    stringstream message;
    cout << "- Type your message. End with a blank line -" << endl;
    string line;
    while(getline(cin, line)) {
        if(line != "") { 
            message << line;
        } else {
            break;
        }
    }
    return message.str();
}

string parseLine(string line) {
    stringstream command;
    stringstream input(line);
    vector<string> fields;

    for(string word; input >> word; ) {
        fields.push_back(word);        
    }

    if(fields.size() == 0) {
        return("0");
    }
    if(fields[0] == "quit") {
       exit(EXIT_SUCCESS);

    }
    if(fields[0] == "send") {
        if(fields.size() == 3) {
            string name = fields[1];
            string subject = fields[2];

            string message = getMessage();
            // string message = "hard coded message";
            command << "put " << name << " " << subject << " " << message.length() <<  "\n" << message;
            return command.str();
        }

    }
    if(fields[0] == "list") {
        if(fields.size() == 2) {
            string name = fields[1];
            command << "list " << name << "\n";
            return command.str();
        }

    }
    if(fields[0] == "read") {
        if(fields.size() == 3) {
            string name = fields[1];
            string index = fields[2];

            command << "get " << name << " " << index << "\n";
            return command.str();
        }
    }
    return "error";
}

void Client::echo() {
    string line;
    int count = 0;
    cout << "% ";
    
    // loop to handle user interface
    while (getline(cin,line)) {
        //parse line
        line = parseLine(line);
        if(debug) cout << "Before send_request " << endl << line << endl; 
        if(line != "error" && line != "0") {
            // send request
            bool success = send_request(line);
            // break if an error occurred
            if (not success)
                break;
            // get a response
            success = get_response();
            // break if an error occurred
            if (not success)
                break;
        } else if(line == "error") {
            cout << "I don't recognize that command\n";
        }
        cout << "% ";
    }
    close_socket();
}

bool Client::send_request(string request) {
    if(debug) cout << "request " << request << endl;
    // prepare to send request
    const char* ptr = request.c_str();
    int nleft = request.length();
    int nwritten;
    // loop to be sure it is all sent
    while (nleft) {
        if ((nwritten = send(server_, ptr, nleft, 0)) < 0) {
            if (errno == EINTR) {
                // the socket call was interrupted -- try again
                continue;
            } else {
                // an error occurred, so break out
                perror("write");
                return false;
            }
        } else if (nwritten == 0) {
            // the socket is closed
            return false;
        }
        nleft -= nwritten;
        ptr += nwritten;
    }
    return true;
}

string parseResponse(string response) {
    stringstream ss(response);
    stringstream m;
    vector<string> fields;
    vector<string> commands;
    string message;
    string line;

    while(std::getline(ss,line,'\n')) {
        commands.push_back(line);
    }

    stringstream command(commands[0]); 

    for(string word; command >> word; ) {
        fields.push_back(word);        
    }

    if(fields.size() == 0) {
        return "Server returned bad message\n";
    }

    if(fields[0] == "OK") {
        return "";
    }

    if(fields[0] == "list") {
        stringstream r;
        for(int i=1; i<commands.size(); i++) {
            r << commands[i] << "\n";
        }
        return r.str();
    }

    if(fields[0] == "message") {
        stringstream m;
        string subject = fields[1];
        int length = atoi(fields[2].c_str());

        m << subject << "\n";
        for(int i=1; i< commands.size(); i++) {
            m << commands[i] << "\n";
        }
     
        return m.str();
    }

    if(fields[0] == "error") {
        cout << "*** response from put" << endl;
        return response;
    }
    return "Server returned bad message\n";
}

bool Client::get_response() {
    string response = "";
    // read until we get a newline
    while (response.find("\n") == string::npos) {
        int nread = recv(server_,buf_,1024,0);
        if (nread < 0) {
            if (errno == EINTR)
                // the socket call was interrupted -- try again
                continue;
            else
                // an error occurred, so break out
                return "";
        } else if (nread == 0) {
            // the socket is closed
            return "";
        }
        // be sure to use append in case we have binary data
        response.append(buf_,nread);
    }
    // a better client would cut off anything after the newline and
    // save it in a cache
    response = parseResponse(response);
    cout << response;
    return true;
}
