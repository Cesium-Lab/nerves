#include <stdlib.h>
#include <sys/types.h>


// DO NOT RUN THIS
// DO NOT RUN THE FOLLOWING COMMANDS
/*

gcc -o out i-forked-up.c
./out

*/

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        char *args[] = {"./out", NULL};
        execvp(args[0], args);
    }

    return 0;
}