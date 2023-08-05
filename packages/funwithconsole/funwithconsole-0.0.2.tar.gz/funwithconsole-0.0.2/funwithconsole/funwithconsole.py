from random import randrange

class draw:

    #region letters1
    letters = {

    "a" : [["     **     "],
        ["    *  *    "],
        ["   ******   "],
        ["  *      *  "],
        [" *        * "]],

    "b" : [[" *****  "],
        [" *    * "],
        [" *****  "],
        [" *    * "],
        [" *****  "]],

    "c" : [[" ***** "],
        [" *     "],
        [" *     "],
        [" *     "],
        [" ***** "]],

    "d" : [[" *****   "],
        [" *    *  "],
        [" *     * "],
        [" *    *  "],
        [" *****   "]],

    "e" : [[" ***** "],
        [" *     "],
        [" ***** "],
        [" *     "],
        [" ***** "]],

    "f" : [[" ***** "],
        [" *     "],
        [" ***** "],
        [" *     "],
        [" *    "]],

    "g" : [[" ***** "],
        [" *     "],
        [" *  ** "],
        [" *   * "],
        [" ***** "]],

    "h" : [[" *   * "],
        [" *   * "],
        [" ***** "],
        [" *   * "],
        [" *   * "]],

    "i" : [[" * "],
            [" * "],
            [" * "],
            [" * "],
            [" * "]],

    "j" : [["   * "],
        ["   * "],
        ["   * "],
        [" * * "],
        [" *** "]],

    "k" : [[" *  * "],
        [" * *  "],
        [" **   "],
        [" * *  "],
        [" *  * "]],

    "l" : [[" *     "],
        [" *     "],
        [" *     "],
        [" *     "],
        [" ***** "]],

    "m" : [[" *          * "],
        [" * *      * * "],
        [" *  *    *  * "],
        [" *   *  *   * "],
        [" *    **    * "]],

    "n" : [[" **    * "],
        [" * *   * "],
        [" *  *  * "],
        [" *   * * "],
        [" *    ** "]],

    "o" : [[" ***** "],
        [" *   * "],
        [" *   * "],
        [" *   * "],
        [" ***** "]],

    "p" : [[" ***** "],
        [" *   * "],
        [" ***** "],
        [" *     "],
        [" *     "]],

    "q" : [[" *****   "],
        [" *   *   "],
        [" *   *   "],
        [" *  **   "],
        [" ***** * "]],

    "r" : [[" ***** "],
        [" *   * "],
        [" ***** "],
        [" *  *  "],
        [" *   * "]],

    "s" : [[" ***** "],
        [" *     "],
        [" ***** "],
        ["     * "],
        [" ***** "]],

    "t" : [[" ***** "],
        ["   *   "],
        ["   *   "],
        ["   *   "],
        ["   *   "]],

    "u" : [[" *   * "],
        [" *   * "],
        [" *   * "],
        [" *   * "],
        [" ***** "]],

    "v" : [[" *       * "],
        ["  *     *  "],
        ["   *   *   "],
        ["    * *    "],
        ["     *     "]],

    "w" : [[" *        **        * "],
        ["  *      *  *      *  "],
        ["   *    *    *    *   "],
        ["    *  *      *  *    "],
        ["     **        **     "]],

    "x" : [[" *   * "],
        ["  * *  "],
        ["   *   "],
        ["  * *  "],
        [" *   * "]],

    "y" : [[" *   * "],
        ["  * *  "],
        ["   *   "],
        ["   *   "],
        ["   *   "]],

    "z" : [[" ***** "],
        ["    *  "],
        ["  ***  "],
        ["  *    "],
        [" ***** "]],

    "0" : [[" ***** "],
        [" *   * "],
        [" *   * "],
        [" *   * "],
        [" ***** "]],

    "1" : [["   *   "],
        [" * *   "],
        ["   *   "],
        ["   *   "],
        [" ***** "]],

    "2" : [["  ***** "],
        ["    *  "],
        ["   *   "],
        ["  *    "],
        [" ***** "]],

    "3" : [[" ***** "],
        ["     * "],
        [" ***** "],
        ["     * "],
        [" ***** "]],

    "4" : [["    *  "],
        ["   **  "],
        ["  * *  "],
        [" ***** "],
        ["    *  "]],

    "5" : [[" ***** "],
        [" *     "],
        [" ***** "],
        ["     * "],
        [" ***** "]],

    "6" : [[" ***** "],
        [" *     "],
        [" ***** "],
        [" *   * "],
        [" ***** "]],

    "7" : [[" ***** "],
        ["    *  "],
        ["   *   "],
        ["  *    "],
        [" *     "]],

    "8" : [[" ***** "],
        [" *   * "],
        [" ***** "],
        [" *   * "],
        [" ***** "]],

    "9" : [[" ***** "],
        [" *   * "],
        [" ***** "],
        ["     * "],
        [" ***** "]],

    " " : [["  "],
        ["  "],
        ["  "],
        ["  "],
        ["  "]]
        
    }
    #endregion letters



    def drawString(self, string, string_char = "*"):
        """This function takes a string input and draws it as big letters to console."""

        letter_line_size = 5
        string = string.lower()

        for letter_line in range(letter_line_size):
            for letter in string:
                
                #get the line from the dictionary [letter_line:letter_line+1] every letter is a 2d list and we need first element [0][0]
                line = self.letters.get(letter)[letter_line:letter_line+1][0][0]
                #replace * with string_char and also add extra spaces if user entered a string with more than one character
                line = line.replace("*", string_char).replace(" "," "*len(string_char))

                print(line, end="")

            print("")

        
    def drawTriangle1(self, shape_size = 10, shape_char = "*"):
        """This function draws type 1 triangle."""
        for i in range(shape_size):
            for j in range(shape_size):
                if(j <= i):
                    print(" " + shape_char + " ", end="")
            print("")


    def drawTriangle2(self, shape_size = 10, shape_char = "*"):
        """This function draws type 2 triangle."""
        for i in range(shape_size):
            for j in range(shape_size):
                if(j >= i):
                    print(" " + shape_char + " ", end="")
            print("")


    def drawTriangle3(self, shape_size = 10, shape_char = "*"):
        """This function draws type 3 triangle."""
        for i in range(shape_size):
            for j in range(shape_size):
                if(j <= i):
                    print("   ", end="")
            for j in range(shape_size):
                if(j >= i):
                    print(" " + shape_char + " ", end="")
            print("")
    

    def drawTriangle4(self, shape_size = 10, shape_char = "*"):
        """This function draws type 4 triangle."""
        for i in range(shape_size):
            for j in range(shape_size):
                if(j >= i):
                    print("   ", end="")
            for j in range(shape_size):
                if(j <= i):
                    print(" " + shape_char + " ", end="")
            print("")


    def drawTriangle5(self, shape_size = 10, shape_char = "*"):
        """This function draws type 5 triangle."""

        shape_size = int(shape_size / 2)
        for i in range(shape_size):

            for j in range(shape_size):
                if(j < shape_size - i):
                    print("   ", end="")

            for j in range(shape_size):
                if(j <= i):
                    print(" " + shape_char + " ", end="")
            
            for j in range(shape_size):
                if(j < i):
                    print(" " + shape_char + " ", end="")

            print("")


    def drawTriangle6(self, shape_size = 10, shape_char = "*"):
        """This function draws type 6 triangle."""

        shape_size = int(shape_size / 2)
        for i in range(shape_size):

            for j in range(shape_size):
                if(j <= i):
                    print("   ", end="")

            for j in range(shape_size):
                if(j < shape_size - i):
                    print(" " + shape_char + " ", end="")

            for j in range(shape_size):
                if(j > i):
                    print(" " + shape_char + " ", end="")

            print("")


    def drawSquare(self, shape_size = 10, shape_char = "*"):
        """This function draws square."""
        for i in range(shape_size):
            for j in range(shape_size):
                print(" " + shape_char + " ", end="")
            print("")


    def drawRectangle(self, shape_size_x = 10, shape_size_y = 5, shape_char = "*"):
        """This function draws rectangle."""
        for i in range(shape_size_y):
            for j in range(shape_size_x):
                print(" " + shape_char + " ", end="")
            print("")


    def drawDiamond(self, shape_size = 10, shape_char = "*"):
        """This function draws a diamond shape."""

        shape_size = int(shape_size / 2)
        for i in range(shape_size):

            for j in range(shape_size):
                if(j < shape_size - i):
                    print("   ", end="")

            for j in range(shape_size):
                if(j <= i):
                    print(" " + shape_char + " ", end="")
            
            for j in range(shape_size):
                if(j < i):
                    print(" " + shape_char + " ", end="")

            print("")

        for i in range(1, shape_size):

            for j in range(shape_size):
                if(j <= i):
                    print("   ", end="")

            for j in range(shape_size):
                if(j < shape_size - i):
                    print(" " + shape_char + " ", end="")

            for j in range(shape_size):
                if(j > i):
                    print(" " + shape_char + " ", end="")

            print("")


    def giveMeChristmas(self, tree_size = 17, tree_layer_size = 5, tree_char = "*", tree_decoration_char = "0"):
        """
        This function draws a christmas tree with decorations.
        * You can change the aperance of the tree by changing tree_char.
        * You can change the decorations of the tree by changing tree_decoration_char.
        * You can change the siz of the tree by changing tree_size, it works better with values bigger than 15.
        * You can change the layer size of the tree by changing tree_layer_size, it could look bad depending on the tree_size.
        """
        
        #to create an equilateral triangle this function crates two right triangles so size should be half
        tree_size = int(tree_size / 2)

        for layer_index in range(tree_layer_size):

            #creating a size difference between layers
            tree_size_factor = tree_layer_size - layer_index
            dynamic_tree_size =  tree_size - tree_size_factor


            #we should cut some of the layer if it is not the first layer
            if(layer_index == 0):
                cut_the_top = 0
            else:
                cut_the_top = int(dynamic_tree_size/tree_layer_size+1)


            #top
            for i in range(cut_the_top, dynamic_tree_size):

                #adding some extra spaces for compansading size difference on the layers
                for j in range(tree_size - dynamic_tree_size):
                    print("   ", end="")

                #adding invisible triangle 
                for j in range(dynamic_tree_size):
                    if(j < dynamic_tree_size - i):
                        print("   ", end="")

                #adding first half of the triangle and random decorations
                for j in range(dynamic_tree_size):
                    if(j <= i):
                        if(randrange(10) == 0):
                            print(" " + tree_decoration_char + " ", end="")
                        else:
                            print(" " + tree_char + " ", end="")
                
                #adding second half of the triangle and random decorations
                for j in range(dynamic_tree_size):
                    if(j < i):
                        if(randrange(10) == 0):
                            print(" " + tree_decoration_char + " ", end="")
                        else:
                            print(" " + tree_char + " ", end="")

                print("")


        #bottom
        for i in range(tree_size):
            for j in range(tree_size*2):
                if(j > (tree_size/2)+1 and j < tree_size + (tree_size/2)-1):
                    print(" " + tree_char + " ", end="")
                else:
                    print("   ", end="")
            print("")





draw = draw()

draw.drawString("console", string_char="//")

        
					
