## funwithconsole

- **Draws strings as big letters to console**

- **Draws christmas tree**

- **Draws various shapes** 


## Install

```sh
pip install funwithconsole
```

## Usage

```python
from funwithconsole import draw
```

```python
draw = draw()
draw.drawString("HELLO", string_char="HI")
```

```
HI      HI    HIHIHIHIHI    HI            HI            HIHIHIHIHI
HI      HI    HI            HI            HI            HI      HI
HIHIHIHIHI    HIHIHIHIHI    HI            HI            HI      HI
HI      HI    HI            HI            HI            HI      HI
HI      HI    HIHIHIHIHI    HIHIHIHIHI    HIHIHIHIHI    HIHIHIHIHI
```

```python
draw.drawString("console", string_char="//")
```

```
//////////    //////////    ////        //    //////////    //////////    //            //////////
//            //      //    //  //      //    //            //      //    //            //
//            //      //    //    //    //    //////////    //      //    //            //////////
//            //      //    //      //  //            //    //      //    //            //
//////////    //////////    //        ////    //////////    //////////    //////////    //////////
```

```python
draw.drawTriangle1(shape_size=10, shape_char="hi")
```

```
 hi
 hi  hi
 hi  hi  hi
 hi  hi  hi  hi
 hi  hi  hi  hi  hi
 hi  hi  hi  hi  hi  hi
 hi  hi  hi  hi  hi  hi  hi
 hi  hi  hi  hi  hi  hi  hi  hi
 hi  hi  hi  hi  hi  hi  hi  hi  hi
 hi  hi  hi  hi  hi  hi  hi  hi  hi  hi
```

```python
draw.giveMeChristmas()
```

```
                         *
                      *  *  *
                   *  *  *  *  *
                      0  *  *
                   0  *  *  0  0
                *  *  *  *  *  0  *
                   *  *  *  *  *
                *  *  *  *  *  *  *
             *  *  *  *  *  *  *  0  *
                   0  *  *  *  *
                *  *  *  *  *  *  *
             *  *  *  *  *  *  *  *  *
          *  *  *  *  *  *  *  *  *  *  *
                   *  *  0  *  *
                *  *  *  *  *  *  0
             *  *  *  *  0  *  *  *  *
          *  *  *  *  *  *  *  *  0  *  *
       *  *  *  *  *  0  *  *  *  *  *  0  *
                   *  *  *  *  *
                   *  *  *  *  *
                   *  *  *  *  *
                   *  *  *  *  *
                   *  *  *  *  *
                   *  *  *  *  *
                   *  *  *  *  *
                   *  *  *  *  *
```

