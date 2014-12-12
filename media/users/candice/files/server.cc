#include "server.h"

map<string, vector<string> > storedMessages;
bool debug = false;
string cache;
queue<int> clientQueue;

Server::Server() {
    // setup variables
    buflen_ = 1024;
    buf_ = new char[buflen_+1];
    sem_init(&s, 0, 1);
    sem_init(&n, 0, 1);
    sem_init(&e, 0, buflen_);
    sem_init(&m, 0, 1);
}

Server::~Server() {
    delete buf_;
}

void Server::run() {
    // create and run the server
    create();
    serve();
}

void Server::create() {
}

void Server::close_socket() {
}

void Server::serve() {
    // setup client
    int client;
    struct sockaddr_in client_addr;
    socklen_t clientlen = sizeof(client_addr);

    pthread_t threads;
    for(int i=0; i<10; i++) {
        pthread_create(&threads, NULL, runThread, &args);
    }

    // producer
    while ((client = accept(server_,(struct sockaddr *)&client_addr,&clientlen)) > 0) {
        sem_wait($e);
        sem_wait(&s);
        clientQueue.push(client);
        sem_post(&s);
        sem_post(&n);
    }
    close_socket();
}

void* Server::runThread(void* args) {
    while(true) {
        sem_wait(&n);
        sem_wait(&s);
        int client = clientQueue.pop();
        sem_post(&s);
        sem_post(&e);
        handleClient(client); // client is a socket descriptor taken from a queue declare
    }
    //d as a class variable
}

string storeMessage(string name, string subject, string message) {
  sem_wait(&m);

  storedMessages[name].push_back(subject);
  storedMessages[name].push_back(message);

  if(storedMessages.find(name) != storedMessages.end()) {
    for(int i=0; i< storedMessages.find(name)->second.size(); i++) {
        if(debug) cout << storedMessages.find(name)->second[i] << " ";
    }
  }

  sem_post(&m);
  return "OK\n";
}

string getList(string name) {
    sem_wait(&m);

    stringstream messages;
    messages << "list ";

    if(storedMessages.find(name) != storedMessages.end()) {
        int size = storedMessages.find(name)->second.size()/2;
        messages << size << "\n";

        int j = 1;
        for(int i=0; i< storedMessages.find(name)->second.size(); i++) {
            if(i % 2 == 0) {
                messages << j << " " << storedMessages.find(name)->second[i] << "\n";
                cout << j << " " << storedMessages.find(name)->second[i] << "\n";
                j++;
            } 
        } 
        if(debug) cout << "getList return message" << messages.str() << endl;

        sem_post(&m);
        return messages.str();  
    }

    sem_post(&m);
    return "error description\n";
}

string getMessage(string name, int index) {
    sem_wait(&m);

    if(debug) cout << "in get message" << endl;
    if(debug) cout << "name " << name << endl;
    if(debug) cout << "index " << index << endl;

    index = (index-1)*2;
    stringstream message;
    message << "message ";
    if(storedMessages.find(name) != storedMessages.end()) {
        for(int i=0; i< storedMessages.find(name)->second.size(); i++) {
            if(debug) cout << storedMessages.find(name)->second[i] << " ";

            string subject = storedMessages.find(name)->second[index];
            string m = storedMessages.find(name)->second[index+1];
            int size = m.length();
            message << subject << " " << size << "\n" << m;

            sem_post(&m);
            return message.str(); 
        }  
    } else {
        sem_post(&m);
        return "error no such message for that user\n";
    }
}

string Server::parseRequest(string request, int client) {
    // cout << request << endl;
    stringstream ss(request);
    stringstream m;
    vector<string> fields;
    vector<string> commands;
    string message;
    string response;
    string line;

    while(std::getline(ss,line,'\n')) {
        // cout << line << endl;
        commands.push_back(line);
    }

    // cout << commands.size() << endl;

    stringstream command(commands[0]); 

    for(string word; command >> word; ) {
        fields.push_back(word);        
    }

    if(fields.size() == 0) {
        if(debug) cout << "size = 0" << endl;
        return "error invalid message\n";
    }

    if(fields[0] == "reset") {
        if(debug) cout << "reset " << endl;
        storedMessages.clear();
        return "OK\n";
    }

    if(fields[0] == "put") {
        if(debug) cout << "put" << endl;

        //read in first 3 strings
        if(fields.size() > 3) {
            string name = fields[1];
            string subject = fields[2];
            int length = atoi(fields[3].c_str());
            string message = get_requestBody(client, length);
            response = storeMessage(name, subject, message);
            // // cout << "response " << response << endl;
            return response;

        } else {
            return "error invalid message\n";
        }
    }

    if(fields[0] == "list") {
        if(debug) cout << "list" << endl;
        if(fields.size() == 2) {
            string name = fields[1];
            response = getList(name);
            if(debug) cout << "response " << response << endl;
            return response;

        } else {
            return "error invalid message\n";
        }
        return "error invalid message\n";

    }

    if(fields[0] == "get") {
        if(debug) cout << "get" << endl;
        if(fields.size() == 3) {
            string name = fields[1];
            int index = atoi(fields[2].c_str());
            response = getMessage(name, index);
            return response;

        } else {
            return "error invalid message\n";
        }
    }
    return "error invalid message\n";
}

void Server::handle(int client) {
    // loop to handle all requests
    while (1) {
        // get a request
        string request = get_request(client);
        // break if client is done or an error occurred
        if (request.empty())
            break;
        // send response
        request = parseRequest(request, client);
        bool success = send_response(client,request);
        if(debug) cout << "after sent response " << success << endl;
        // break if an error occurred
        if (not success)
            break;
    }
    close(client);
}

string Server::get_requestBody(int client, int length) {
    string request = "";
    // read until we get a newline
    while (cache.length() < length) {
        int nread = recv(client,buf_,1024,0);
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
        cache.append(buf_,nread);
    }

    request = cache.substr(0, length);
    cache.erase(0, length);

    // a better server would cut off anything after the newline and
    // save it in a cache
    return request;
}

string Server::get_request(int client) {
    if(debug) cout << "getting request" << endl;
    string request = "";
    // read until we get a newline
    while (cache.find("\n") == string::npos) {
        if(debug) cout << "here..." << endl;
        int nread = recv(client,buf_,1024,0);
        cout << "nread" << nread << endl;
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
        cache.append(buf_,nread);
    }

    int position = cache.find("\n");
    if(debug) cout << "position " << position << endl;
    request = cache.substr(0, position + 1);
    cache.erase(0, position +1);

    // a better server would cut off anything after the newline and
    // save it in a cache
    if(debug) cout << "request" << endl;
    return request;
}

bool Server::send_response(int client, string response) {
    if(debug) cout << "sending response" << endl;
    // prepare to send response
    const char* ptr = response.c_str();
    int nleft = response.length();
    int nwritten;
    // loop to be sure it is all sent
    while (nleft) {
        if ((nwritten = send(client, ptr, nleft, 0)) < 0) {
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
    if(debug) cout << "finished response" << endl;
    return true;
}

