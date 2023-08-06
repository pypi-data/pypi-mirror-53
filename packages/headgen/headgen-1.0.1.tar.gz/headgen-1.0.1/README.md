# `C headers` files generator
# I GIVE NO WARRANTY FOR YOU UNSAFE MOVES)

This is util for `generating headers files`.
You should learn very small
syntax for this program (much more `easier`)

## Working principle

After running this util will find all `*.c`
files in current and subdirectories and
read special syntax for getting information.
After it, this program creates a header file 
for the current file.

# Syntax

#### Functions
Simple example for function
```c
int sum_integers(int first, int second) //&signature
{
    return first + second;
}
```
Simple example for function with documentation
Just add `//&documentation` before doc
Does not work inside function!
```c
//&documentation
/*!
@brief add two numbers
@param[in] int first number
@param[in] int second number
@return int 
*/
int sum_integers(int first, int second) //&signature
{
    return first + second;
}
```
# Structures

Just add `/*&structure` before struct
```c
/*&structure
typedef struct 
{
    int a;
    int b;
} example
*/
```
# Enums
Just add `//&structure` before struct
```c
/*&enum
enum codes
{
    no error,
    error,
};

*/
```

# Defines
```c
/*&defines
#define 1 0 
#define and or
#define + -
#define * /
*/
```

# Includes 
You do not have to write
`#include`before name
```c
/*&includes
<math.h>
"your_lib.h"
<string.h>
<stdio.h>
*/
```
#### Result
```с
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "your_lib.h"
```


# Flags

|Short flag | Long flag | Description | Default | 
|----|----|----|----|
| `-p` | `--pragma` | Sets protection with pragma | False|
|`-if`|`--ifndef`| Sets protection with ifndef | True|
| `-i` | `--info` | Adds info on top of the file | True|
|`-enc`|`--encoding`| Sets encoding of thу file |`utf-8`|

# Links
- [Github link](https://github.com/YoungMeatBoy/headgen.git)
- Email : `d2ms2nk@gmail.com`

## On any issue report in GitHub!