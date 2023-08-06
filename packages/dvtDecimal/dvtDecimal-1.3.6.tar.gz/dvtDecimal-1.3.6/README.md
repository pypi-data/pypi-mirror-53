Recent changes:

* add some (La)TeX output (see bottom of this page)

* change `contFractionQ` function output


This package provides a way to access repeating decimals in the
decimal representation of rational numbers.

### class object

``` python3
>>> from dvtDecimal import *

```


Once package importation completed, you have to create a rational
number using:

* a fraction representation


``` python3
>>> f = dvtDecimal(-604, 260)

```

for the fraction whose numerator is -604 and denominator is 260.


* or a decimal representation, it could be an integer

``` python3
>>> f = dvtDecimal(2.5)

```

* or repeating decimals as a string

``` python3
>>> f = dvtDecimal('00765')

```

thus creating a number (w/o irregular part) between 0 and 1.
In the example, 0.007650076500765... and so on.


### object methods and variables

Once you created the object, you can access to those variables:


``` python3
>>> f.initValues
[-604, 260]
>>> f.simpValues
[-151, 65]
>>> f.intPart
-2
>>> f.repPart
[2, 3, 0, 7, 6, 9]
>>> f.sign
-1
>>> f.gcd
4

```

and to those methods:


``` python3
>>> f.fraction()
-604/260
>>> f.irrPart()
0.3
>>> f.repPartC()
230769
>>> f.periodLen()
6
>>> f.mixedF()
[-2, 21, 65]
>>> f.isDecimal()
False
>>> f.dotWrite(20)
-2.32307692307692307692
>>> f.dispResults()
For fraction: -604/260
    integer   part : -2
    irregular part : 0.3
    periodic  part : [2, 3, 0, 7, 6, 9]
    mixed fraction : [-2, 21, 65]
    simp. fraction : [-151, 65]
               gcd : 4
    Python outputs : -2.3230769230769233

```

Entering via repeating decimals string allows:

``` python3
>>> f = dvtDecimal('0123456789')
>>> f.simpValues
[13717421, 1111111111]

```


dvtDecimal also supports minimal operations (+,-,*,/) in between
elements of the class but also with integers:


``` python3
>>> f = dvtDecimal(1, 5)
>>> g = dvtDecimal(10, 3)
>>> h = f + g
>>> h.mixedF()
[3, 8, 15]
>>> i = f / g
>>> i.mixedF()
[0, 3, 50]

```

``` python3
>>> f = dvtDecimal(1, 5)
>>> g = 5
>>> h = f * g
>>> h.isDecimal()
True

```


``` python3
>>> f = dvtDecimal(1, 5)
>>> g = dvtDecimal(7, 5)
>>> h = f - g
>>> h.simpValues
[-6, 5]

```


### egyptian fractions

IMPORTANT 1: Egyptian fractions features are quite slow (could be
VERY slow) because it uses dvtDecimal representation of numbers
(unlike previous versions).  As it doesn't use algebraic
computation, you have to untrust some results or at least to verify
them with another method...

IMPORTANT 2: This part gives you results for the fractionnal part of
the rational number you work with i.e. the last two numbers in the
`mixedF` list, so that you only get results for <=1 fractions.


dvtDecimal provides the method `egyptFractions` to get `all` the
egyptian fractions equal to your current fraction.

`egyptFractions` outputs a list of lists. Each of these lists are
denominators (increasing) for unitary fractions whose sum equals to
your fraction.

Two optional arguments:
* `eF` number of fractions in the sums, default is `3`
* `lim` max. number of solutions in the results, default is `10`
* `lim` can be `0` for **all** fractions!



``` python3
>>> f = dvtDecimal(18,5)
>>> f.mixedF()
[3, 3, 5]
>>> f.egyptFractions()
[[2, 11, 110], [2, 12, 60], [2, 14, 35], [2, 15, 30], [2, 20, 20], [3, 4, 60], [3, 5, 15], [3, 6, 10]]
>>> f.egyptFractions(lim=5)
[[2, 11, 110], [2, 12, 60], [2, 14, 35], [2, 15, 30], [3, 4, 60]]
>>> f.egyptFractions(eF=4, lim=1)
[[2, 11, 111, 12210]]
>>> f.egyptFractions(eF=4, lim=0)
[[2, 11, 111, 12210], [2, 11, 112, 6160], [2, 11, 114, 3135], [2, 11, 115, 2530], [2, 11, 120, 1320], [2, 11, 121, 1210], [2, 11, 130, 715], [2, 11, 132, 660], [2, 11, 135, 594], [2, 11, 154, 385], [2, 11, 160, 352], [2, 11, 165, 330], [2, 11, 210, 231], [2, 12, 61, 3660], [2, 12, 62, 1860], [2, 12, 63, 1260], [2, 12, 64, 960], [2, 12, 65, 780], [2, 12, 66, 660], [2, 12, 68, 510], [2, 12, 69, 460], [2, 12, 70, 420], [2, 12, 72, 360], [2, 12, 75, 300], [2, 12, 76, 285], [2, 12, 78, 260], [2, 12, 80, 240], [2, 12, 84, 210], [2, 12, 85, 204], [2, 12, 90, 180], [2, 12, 96, 160], [2, 12, 100, 150], [2, 12, 105, 140], [2, 12, 108, 135], [2, 12, 110, 132], [2, 13, 44, 2860], [2, 13, 45, 1170], [2, 13, 50, 325], [2, 13, 52, 260], [2, 13, 60, 156], [2, 13, 65, 130], [2, 14, 36, 1260], [2, 14, 40, 280], [2, 14, 42, 210], [2, 14, 60, 84], [2, 15, 31, 930], [2, 15, 32, 480], [2, 15, 33, 330], [2, 15, 34, 255], [2, 15, 35, 210], [2, 15, 36, 180], [2, 15, 39, 130], [2, 15, 40, 120], [2, 15, 42, 105], [2, 15, 45, 90], [2, 15, 48, 80], [2, 15, 50, 75], [2, 15, 55, 66], [2, 16, 27, 2160], [2, 16, 28, 560], [2, 16, 30, 240], [2, 16, 32, 160], [2, 16, 35, 112], [2, 16, 40, 80], [2, 16, 48, 60], [2, 17, 25, 850], [2, 17, 34, 85], [2, 18, 23, 1035], [2, 18, 24, 360], [2, 18, 25, 225], [2, 18, 27, 135], [2, 18, 30, 90], [2, 18, 35, 63], [2, 18, 36, 60], [2, 20, 21, 420], [2, 20, 22, 220], [2, 20, 24, 120], [2, 20, 25, 100], [2, 20, 28, 70], [2, 20, 30, 60], [2, 20, 36, 45], [2, 21, 28, 60], [2, 21, 35, 42], [2, 24, 30, 40], [3, 4, 61, 3660], [3, 4, 62, 1860], [3, 4, 63, 1260], [3, 4, 64, 960], [3, 4, 65, 780], [3, 4, 66, 660], [3, 4, 68, 510], [3, 4, 69, 460], [3, 4, 70, 420], [3, 4, 72, 360], [3, 4, 75, 300], [3, 4, 76, 285], [3, 4, 78, 260], [3, 4, 80, 240], [3, 4, 84, 210], [3, 4, 85, 204], [3, 4, 90, 180], [3, 4, 96, 160], [3, 4, 100, 150], [3, 4, 105, 140], [3, 4, 108, 135], [3, 4, 110, 132], [3, 5, 16, 240], [3, 5, 18, 90], [3, 5, 20, 60], [3, 5, 24, 40], [3, 6, 11, 110], [3, 6, 12, 60], [3, 6, 14, 35], [3, 6, 15, 30], [3, 7, 10, 42], [3, 8, 10, 24], [3, 9, 10, 18], [4, 5, 7, 140], [4, 5, 8, 40], [4, 5, 10, 20], [4, 5, 12, 15], [4, 6, 10, 12]]

```

In the above example, egyptian fractions are thus calculated with
fraction 3/5.

First solution `[2, 11, 111, 12210]` (in the last command result)
has to be interpreted as: 3/5 = 1/2 + 1/11 + 1/111 + 1/12210


dvtDecimal also provides `egyptG2` method. This gives you a list
of two denominators of unitary fractions whose sum equals your
fraction.

This is an implementation of **the greedy algorithm**. It gives you
naturally **matching pairs** for unitary fractions input.

The result may be an empty list since all numbers cannot be written
as so.

``` python3
>>> f = dvtDecimal(18,5)
>>> f.intPart
3
>>> f.egyptG2()
[2, 10]

```

So: 18/5 = 3 + 1/2 + 1/10


### continued fractions

#### what is implemented and what is not

you can:

* transform a `dvtDecimal` in a (finite) sequence which terms are integers in the continued fraction representation. This is done with the `contFraction` method;

* get successive rational approximations from a list representing a continued fraction. This is done using `ratApp` function on a list. Output of this function is a list of `dvtDecimal` objects.


you cannot:

* thus so far, no periodic continued fraction forms

* transform irrationals...

#### some examples


* Looking for continued fractions

Below, search for 634 / 75 and for 3.14159265


``` python3

>>> f = dvtDecimal(634, 75)
>>> f.contFraction()
[8, 2, 4, 1, 6]
>>> f = dvtDecimal(3.14159265)
>>> f.contFraction()
[3, 7, 15, 1, 288, 1, 2, 1, 3, 1, 7, 4]

```

Every exact number gives a truthy continued fraction form.

In the latter example, the continued fraction do not represent &#960; for the decimal 3.14159265 is not &#960;

We can observe that numbers are quickly false: true continued fraction of &#960; begins with `[3, 7 15, 1, 292, 1, 1, 1, ...]`


* Looking for rational approximations


``` python3

>>> f = dvtDecimal(634, 75)
>>> c = f.contFraction()
>>> print(ratApp(c))
[<dvtDecimal.dvtDecimal object at 0x7f40b8c9ec18>, <dvtDecimal.dvtDecimal object at 0x7f40b8c9ec50>, <dvtDecimal.dvtDecimal ob
ject at 0x7f40b8c9ec88>, <dvtDecimal.dvtDecimal object at 0x7f40b8c9ecc0>, <dvtDecimal.dvtDecimal object at 0x7f40b8c9ecf8>]
>>> for d in ratApp(c):
        print("{:<1}+{:>3}/{:<2}  {:<11}".format(*d.mixedF(), d.dotWrite(10)))
8+  0/1   8.0000000000
8+  1/2   8.5000000000
8+  4/9   8.4444444444
8+  5/11  8.4545454545
8+ 34/75  8.4533333333
>>> f = dvtDecimal(3.14159265)
>>> c = f.contFraction()
>>> for d in ratApp(c):
        print("{:<1}+{:>7}/{:<8}  {:<8}".format(*d.mixedF(), d.dotWrite(15)))
3+      0/1         3.000000000000000
3+      1/7         3.142857142857142
3+     15/106       3.141509433962264
3+     16/113       3.141592920353982
3+   4623/32650     3.141592649310872
3+   4639/32763     3.141592650245703
3+  13901/98176     3.141592649934810
3+  18540/130939    3.141592650012601
3+  69521/490993    3.141592649997046
3+  88061/621932    3.141592650000321
3+ 685948/4844517   3.141592649999989
3+2831853/20000000  3.141592650000000

```


The solar year is approximately 365 days, 5 hours, 48 minutes and 45.198 seconds leading to `365.2421898` days (see [Wikipedia](https://fr.wikipedia.org/wiki/Ann%C3%A9e_tropique#Dur%C3%A9e)).

Let's play with this!

We are going to round this number with a precision from 1 to 7
digits then transform in continued fractions and find all the
rational approx. given by these numbers using a mixed fraction. As
some approx. will be equal, get unique representations and sort
then using numerators (in mixed form).


``` python3

>>> aS = 365.2421898
>>> mF = []
>>> for a in range(7):
        aaS = round(aS,7-a)
        f = dvtDecimal(aaS)
        c = f.contFraction()
        for d in ratApp(c):
            mF+=[d.mixedF()]

```

OK! I got all my mixed fractions from all roundings. I, now, create
a list of uniques since a lot of them are equal, for this I've used [this code from StackOverflow](https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists):

``` python3

>>> mF = [list(x) for x in set(tuple(x) for x in mF)]
>>> mF.sort(key=lambda l:l[1])
>>> mF
[[365, 0, 1], [365, 1, 5], [365, 1, 4], [365, 6, 25], [365, 7, 29], [365, 8, 33], [365, 15, 62], [365, 31, 128], [365, 53, 219
], [365, 121, 500], [365, 132, 545], [365, 163, 673], [365, 295, 1218], [365, 458, 1891], [365, 752, 3105], [365, 814, 3361], 
[365, 1211, 5000], [365, 2473, 10211], [365, 3287, 13572], [365, 4543, 18758], [365, 5760, 23783], [365, 9838, 40621], [365, 1
4807, 61138], [365, 20567, 84921], [365, 24219, 100000], [365, 35374, 146059], [365, 126689, 523098], [365, 542130, 2238451], 
[365, 1210949, 5000000]]

```

This done, it's difficult to use for deciding leap years since
denominators are quite maladjusted except for 5, 4, 25, 500, 5000,
100000, and 5000000. Now looking at numerators for these fractions, we recognize 1 year out of 4 and that's all! Where is 97 out of 400?

Actually, we do not use `365.2421898` but `365.2425`, let's see
with it:

``` python3

>>> f = dvtDecimal(365.2425)
>>> c = f.contFraction()
>>> for d in ratApp(c):
        print("{:<1}+{:>3}/{:<3}  {:<4}".format(*d.mixedF(), d.dotWrite(4)))
365+  0/1    365.0000
365+  1/4    365.2500
365+  8/33   365.2424
365+ 97/400  365.2425

```


* Continued fraction of a quadratic non rational number

`contFractionQ` function (it's not a method!) provides this:


``` python3

>>> import math
>>> contFractionQ(math.sqrt(2019))
[44, [1, 13, 1, 88]]

```

The nested list is the periodic part of the continued fraction.


### (La)TeX output

Since 1.3.0 version, `dvtDecimal` offers some (La)TeX output
functions. Actullaly this is native TeX, so that it doesn't require
any special package.

MY usage is to format continued fractions with `\displaystyle`, if
you don't want them, just search and destroy with your (La)TeX
editor!


* `toTeX` method for `dvtDecimal` objects

Outputs fraction (w/o dps!), mixed fraction and decimal
representation.

``` python3

>>> f = dvtDecimal(1, 7)
>>> f.toTeX()
['{1\\over7}', '{0\\raise.21em\\hbox{$\\scriptscriptstyle\\frac{1}{7}$}}', '0.\\overline{142857}']
>>> print(f.toTex()[1])
{0\raise.21em\hbox{$\scriptscriptstyle\frac{1}{7}$}}

```

* `egToTeX` function

Outputs egyptian fractions sum for list as argument. The list is
typically output of the `egyptG2` method.

``` python3

>>> f = dvtDecimal(1, 7)
>>> f.egyptG2()
[8, 56]
>>> egToTeX(f.egyptG2())
'{1\\over8}+{1\\over56}'
>>> print(egToTeX(f.egyptG2()))
{1\over8}+{1\over56}

```

* continued fractions functions: `cfToTeX` and `cfQToTeX`

First outputs full continued fraction of a finite (flat)
list. Typically to use with `contFraction` method.

``` python3

>>> f = dvtDecimal(123, 43)
>>> f.contFraction()
[2, 1, 6, 6]
>>> cfToTeX(f.contFraction())
'2+\\displaystyle{\\strut1\\over\\displaystyle1+{\\strut1\\over\\displaystyle6+{\\strut1\\over6}}}'
>>> print(cfToTeX(f.contFraction()))
2+\displaystyle{\strut1\over\displaystyle1+{\strut1\over\displaystyle6+{\strut1\over6}}}

```

Last outputs partial continued fraction of a periodic continued
fraction. Typically to use with `contFractionQ` function.

So the list to provide contains numbers and a list (see
`contFractionQ`) and needs an integer as a second argument: this is
the index of the end, you'll get `\dots` in the last unit fraction.

``` python3

>>> import math
>>> contFractionQ(math.sqrt(23))
[4, [1, 3, 1, 8]]
>>> cfQToTex(contFractionQ(math.sqrt(23)), 7)
[4] [1, 3, 1, 8]
'4+\\displaystyle{\\strut1\\over\\displaystyle1+{\\strut1\\over\\displaystyle3+{\\strut1\\over\\displaystyle1+{\\strut1\\over\\displaystyle8+{\\strut1\\over\\displaystyle1+{\\strut1\\over\\displaystyle3+{\\strut1\\over\\displaystyle\\dots}}}}}}}'
>>> print(cfQToTex(contFractionQ(math.sqrt(23)), 7))
[4] [1, 3, 1, 8]
4+\displaystyle{\strut1\over\displaystyle1+{\strut1\over\displaystyle3+{\strut1\over\displaystyle1+{\strut1\over\displaystyle8+{\strut1\over\displaystyle1+{\strut1\over\displaystyle3+{\strut1\over\displaystyle\dots}}}}}}}

```

### further

I hope to:

* improve `contFractionQ` function and provide a way to
get succesive rational approximations ;

* improve egyptian fractions methods to speed up calculations.


### about

dvtDecimal is rather an attempt to publish on the `PyPi` packages
index than a fully completed python project, I do not recommend
dvtDecimal usage for professionnal use. You have to consider this
package as an experiment.
