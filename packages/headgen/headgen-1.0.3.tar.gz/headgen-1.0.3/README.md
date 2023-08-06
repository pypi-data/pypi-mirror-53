# `C headers` files generator

# Requiers
```
python >= 3.5
```

# Instalation
```bash
pip install headgen
pip3 install headgen
```
# Run
```bash
cd path/to/your/prject
python -m headgen.headgen <flags>
python3 -m headgen.headgen <flags>
```

# Flags

|Short flag|   Long flag   |          Description        | Default | 
|----------|---------------|-----------------------------|---------|
| `-p`     |`--pragma`     | Sets protection with pragma |  False  |
|`-if`     |`--ifndef`     | Sets protection with ifndef |  True   |
| `-i`     |`--info`       | Adds info on top of the file|  True   |
|`-enc`    |`--encoding`   | Sets encoding of thу file   | `utf-8` |
|`-im`     |`--ignore_main`| Ignores main.c file         |  True   |


# Functions

- For automatic adding of the signature of any function
type `//&signature`.

```c
int sum_integers(int first, int second) //&signature
{
    return first + second;
}
```
 - After running to your header file this line will be added
```c
int sum_integers(int first, int second);
```

# Functions with documentation

 - Example for function with documentation
 - Add `//&documentation` before documentation
 - Does not work inside function!

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

#### Added to header:
```c
/*!
@brief add two numbers
@param[in] int first number
@param[in] int second number
@return int 
*/
int sum_integers(int first, int second);
```

# Structures
#### Place the struct you want into:
```c
/*&structure

place typedef struct
or just a struct here

*/
```
#### Example:
```c
/*&structure
typedef struct 
{
    int a;
    int b;
} example
*/
```

#### Added to header:
```c
typedef struct 
{
    int a;
    int b;
} example
```


# Enums
#### Place the enum you want into:
```c
/*&enum

Place enum here

*/
```

#### Example
```c
/*&enum
enum codes
{
    no error,
    error,
};
*/
```
#### Added to header:
```c
enum codes
{
    no error,
    error,
};
```

# Defines
#### Example:
```c
/*&defines
#define 1 0 
#define and or
#define + -
#define * /
*/
```
#### Added to header:
```c
#define 1 0 
#define and or
#define + -
#define * /
```

# Includes 
You do not have to write
`#include` before lib name
#### Example:
```c
/*&includes
<math.h>
"your_lib.h"
<string.h>
<stdio.h>
*/
```
#### Added to header:
```c
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "your_lib.h"
```

# Information at top of the header
- Time of the generation
- Amount of thу functions
- Amount of the documentated functions
- Check if they are all documentated
- Amount of the structures
- Amount of the enums
- Functions names (sorted by alphabet)


# Protection
## `Pragma`
If you want to set protection of your file with `#pragma onсe`
run program with flag `-p`
```bash
python -m headgen.headgen -p True
python -m headgen.headgen --pragma True
```
#### Added to header:
```c
#pragma once
```

## `ifndef` (Defautlt protection)
If you want to set protection of your file with `ifndef`
run program with flag `-if`

```bash
python -m headgen.headgen -if True
python -m headgen.headgen -if True
```
#### Added to header
```c
// Default file is list.h
#ifndef __LIST_H__
#define __LIST_H__

...

#endif // __LIST_H__
```


# Links
- [Github link](https://github.com/YoungMeatBoy/headgen.git)
- Email : `d2ms2nk@gmail.com`

## On any issue report in GitHub!