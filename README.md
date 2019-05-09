# Witz

Witz is your different Object Oriented programming language, a brand new and groovy syntax is what awaits you for you with this next language.
* Object Oriented
* New groovy syntax
* Fun and easy to learn

## Installation

Your computer must meet the following requirements to properly run:
1. Python (at least) version 3.0 installed
2. 

In order to run and execute your program, you would have to type the following in your terminal

```
./witz youprogramname.wit
```

## Documentation
The documentation is divided in two pieces:
* Spanish [tutorial](https://www.youtube.com/watch?v=uEiUCLxxcvU&feature=youtu.be)
* English complete [documentation](https://drive.google.com/file/d/11ghH3XbYckO4Xg_t-iCuJC-9DD_Zps7P/view?usp=sharing)

## Example
We have several [examples](https://github.com/JawnF/Witz/tree/master/tests). Here is the first one to get you started 

```javascript
@dog(name:str, age:int){
    #bark:void() {
        this.age = 10;
        print(name);
    }
    #getage:int(){
        <- this.age;
    }
}

#factorial:int(index:int) {
    $res:int;
    if (index < 2) {
        res = 1;
    } else {
        res = index * factorial(index-1);
    }
    <- res;
}

$fito:dog = new dog('fito', 3);
fito.bark();
print(fito.getage());

$foo:stack(int);

print('Ingrese limite para buscar factorial.');
$limit:int = read();
$i:int = 1;
while (i < limit) {
    foo.push( factorial(i) );
    i = i + 1;
}

$j:int = foo.size();

while (j > 0) {
    print(foo.pop());
    j = foo.size();
}
```

## Syntax
### Class declaration
``` javascript
@classname(attributes){
  
}
```
### Function declaration
``` javacript
#functionname:returntype(param1:type1) {
  <- returnvalue;
}
```
### Variable declaration
``` javascript
$name:type;
$name:type = value;
```
### While loop
``` javascript
while(condition) {

}
```
### If conditional
``` javascript
if(condition) {

}
```
### If-else conditional
``` javascript
if(condition) {

}else {

}
```
## License
Witz was developed for academic purposes only during the Spring period of 2019 for the Compiler Design class at Tecnologico de Monterrey, campus Monterrey.

## Developers
1. [Juan Pablo Ferreira](https://github.com/JawnF)
2. [Karla Robledo Bandala](https://github.com/bandalas)

## Mentors
1. Elda Guadalupe Quiroga
2. Hector Ceballos
