from conversion import Conversion

class State:
    def __init__(self, operation, characters):
        self._kind: str = ""
        self._validCharacters: [str] = characters
        self.determineKind(operation)
        if "e" in self._validCharacters and self._kind == "concat":
            self._validCharacters[0].replace("e", "")
        elif "e" in self._validCharacters and self._kind == "union":
            self._validCharacters.remove("e")

    def determineKind(self, operation):
        if operation == 'U':
            self._kind = "union"
        elif operation == "o":
            self._kind = "concat"
        else:
            self._kind = "invalid"
        
    def validate(self, char):
        if self._kind == "invalid":
            return False

        for x in self._validCharacters:
            print(char)
            print(x)
            if char == x:
                return True
        
        return False

    def validCharacters(self):
        return self._validCharacters

    def kind(self):
        return self._kind

# class Expression:
#     def __init__(self, testCase: str):
#         self._string: str = Conversion(testCase).output()
#         self._symbols: [str] = []
#         for char in self._string:
#             self._symbols.append(char)

#     def symbols(self):
#         return self._symbols

#     def __str__(self):
#         return self._string

class Machine:
    def __init__(self, testCase: str):
        self._expression = Conversion(testCase).output()
        self._stateQueue: [State] = []
        self.createMachine()

    def createMachine(self):
        stack: str = []
        stack2: str = []
        expression: str = []
        for x in self._expression:
            expression.append(x)

        print(expression)

        while len(expression) > 0:
            symbol = expression[0]
            if symbol != "U" and symbol != "o":
                stack.append(symbol)
            elif symbol == "U":
                if len(stack) >= 2:
                    x = stack.pop()
                    y = stack.pop()
                else:
                    x = stack2.pop()
                    y = stack2.pop()
                self._stateQueue.append(State("U", [x, y]))
                stack2.append(x)
                stack2.append(y)
            elif symbol == "o":
                if len(stack) >= 2:
                    x = stack.pop()
                    y = stack.pop()
                else:
                    x = stack2.pop()
                    y = stack2.pop()
                self._stateQueue.append(State("o", [y+x]))
                stack2.append(x)
                stack2.append(y)

            expression.pop(0)

    def validate(self, testCase: str):
        expression: str = ("".join(self._expression))

        print(expression)

        if 'U' not in self._expression and 'o' not in self._expression:
            if testCase == expression:
                return True
            else:
                return False
        else:

            queue = []
            for x in self._stateQueue:
                queue.append(x)
            
            # if it ends with Uo then we remove the remaining o
            if expression[-1] == "o" and expression[len(expression) - 2] == "U":
                expression[:-1]
            # boolean in case we want to skip an iteration
            skip = False

            while len(testCase) > 0:
                if skip == True:
                    skip == False
                    continue
            
                if len(queue) == 0:
                    break
                
                currState = queue.pop(0)

                if currState.kind() == "concat":
                    validCharacter = currState.validCharacters()[0]
                    if len(validCharacter) == 2:
                        skip == True
                        if len(testCase) == 1:
                            return False
                        elif currState.validate(testCase[0] + testCase[1]) == False:
                            return False
                    elif len(validCharacter) == 1:
                        if currState.validate(testCase[0]) == False:
                            return False

                elif currState.kind() == "union":
                    if currState.validate(testCase[0]) == False:
                        return False

                elif currState.kind() == "invalid":
                    return False

                testCase = testCase[1:]

            if len(testCase) > 0:
                return False    

            return True

                    
def tokenizeFile() -> [[str]]:
    with open("mpa2.in") as file:
        inputString: str = file.read()
        inputString = inputString.replace(" ", "")
        cases = inputString.split("\n")

        return cases

def main():
    # tokens = tokenizeFile()
    # for token in tokens:
    #     x = Machine(token)
    #     print(x.validate())
    x = Machine("a U (a U b)")
    print(x.validate("a"))
    print(x.validate("ba"))
    # print(Conversion("ab").output())

if __name__ == "__main__":
    main()