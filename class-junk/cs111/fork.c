#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

void what_the_fork() {

    char* buf = "HOWDY";

    pid_t pid_thing = fork();

    printf("\n");

    if (!pid_thing) {
        printf("Child (addr=%p)\n", &buf);
        buf = "lower";
        printf("String: %s\n", buf);
        printf("(new addr=%p)\n\n", &buf);
        sleep(2);
        exit(0);

    } else {
        printf("----> waiting for child (NO SLEEP IN THIS FUNCTION)\n");
        waitpid(pid_thing, NULL, 0);
        
        printf("----> Parent waited for child! (addr=%p)\n", &buf);
        buf = "upper";
        printf("----> String: %s\n", buf);
        printf("---->(new addr=%p)\n", &buf);
    }

    return;

}

int main() {

    what_the_fork();
    printf("AAAAAAA\n");

    return 0;


}
    