#include"add3.h"
#include "add.h"
int add3(int a, int b, int c) {
    return add(add(a, b), c);
}