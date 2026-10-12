#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int main() {

    execvp("BAD PATH", NULL);
    printf("this should be unsuccessful\n");

    execvp("./SAMPLE", NULL);
    printf("this should not print\n");

    return -1;


}
    