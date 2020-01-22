from abc import ABC, abstractmethod


def hasDataType(line) -> bool:
    if "double" in line or "int" in line or "char" in line or "float" in line or "void" in line or "return" in line:
        return True
    else:
        return False


class Parser(ABC):
    @abstractmethod
    def tokenize(self):
        pass

    @abstractmethod
    def test(self):
        pass


class VariableParser(Parser):
    def __init__(self, testCase: str):
        self._string: str = testCase
        self._tokens: [str] = []
        self._validity: bool = True
        self.tokenize()

    def tokenize(self):
        # makes a list containing the data type at index 0 and everything else at index 1
        self._tokens = self._string.split(" ", 1)
        # sets the trailing string to be used for further tokenization
        trail: str = self._tokens[1] if len(
            self._tokens) > 1 else self._tokens[0]

        # removes trailing string from list of tokens
        self._tokens.pop()

        # tokenizes the string and creates a list using a comma as the delimiter
        for temp in trail.split(","):
            # checks if there is a data type in the string
            if hasDataType(temp):
                for item in temp.split(" "):
                    if item != "":
                        self._tokens.append(item)
            # checks if the string has a newline
            elif "\n" in temp:
                for item in temp.split("\n"):
                    if " " in item:
                        for item in item.split(" "):
                            self._tokens.append(item)
                    elif item != "":
                        # removes the spaces
                        item = item.replace(" ", "")
                        self._tokens.append(item)
            else:
                # removes the spaces
                temp = temp.replace(" ", "")
                self._tokens.append(temp)

    def test(self):
        return

    def tokens(self) -> [str]:
        return self._tokens


class FunctionDeclarationParser(Parser):
    def __init__(self, testCase: str):
        self._string: str = testCase
        self._tokens: [str] = []
        self._validity: bool = True
        self.tokenize()

    def tokenize(self):
        # makes a list containing the data type at index 0 and everything else at index 1
        self._tokens: [str] = self._string.split(" ", 1)
        # since the name is stored somewhere in index 1, we store it in a variable
        trail: str = self._tokens[1]
        # we remove the last item of the list which was everything to the right of the data type
        self._tokens.pop()

        # checks if another function declaration is found
        if '),' in trail:
            # splits the list using ),
            comma: [str] = trail.split('),')
            for item in comma:
                # returns the parenthesis that we removed during split
                item += ')'
                # we try to isolate the name of the function by splitting the trail with the first close parenthesis we see
                temp: [str] = item.split(")", 1)
                # currently the list looks like this: [function name with parameters, everything else]

                # removes everything after the ) from the list
                temp.pop()

                # appends function name while using the open parenthesis as the delimiter
                self._tokens.append(temp[0].split("(")[0])
                # appends list of function parameters while using the open parenthesis as the delimiter and stripping the close parenthesis at the end
                self._tokens.append(VariableParser(
                    temp[0].split("(")[1].strip(")")).tokens())

        else:
            # we try to isolate the name of the function by splitting the trail with the first close parenthesis we see
            temp: [str] = trail.split(")", 1)
            # currently the list looks like this: [function name with parameters, everything else]

            # removes everything after the ) from the list
            temp.pop()

            # appends function name while using the open parenthesis as the delimiter
            self._tokens.append(temp[0].split("(")[0])
            # appends list of function parameters while using the open parenthesis as the delimiter and stripping the close parenthesis at the end
            self._tokens.append(VariableParser(
                temp[0].split("(")[1].strip(")")).tokens())

    def test(self):
        return

    def tokens(self) -> [str]:
        return self._tokens


class FunctionDefinitionParser(Parser):
    def __init__(self, testCase: str):
        self._string: str = testCase
        self._tokens: [str] = []
        self._validity: bool = True
        self.tokenize()

    def tokenize(self):
        # creates a list with the function name in index 0 and everything else at index 1
        self._tokens: str = self._string.split("{", 1)
        trail: str = self._tokens[1].strip()
        trail = trail.strip("}")
        self._tokens.pop()
        # we use the tokenize function from the function declaration class
        self._tokens = FunctionDeclarationParser(self._tokens[0]).tokens()
        lines: [str] = trail.split(";")
        lines.pop()
        operations: [str] = []
        for line in lines:
            # we use the tokenize function from the variable class
            for item in VariableParser(line.strip()).tokens():
                operations.append(item)

        self._tokens.append(operations)

    def test(self):
        return

    def tokens(self) -> [str]:
        return self._tokens


def handleTokenization(testCase) -> [str]:
    if "{" in testCase:
        return FunctionDefinitionParser(testCase).tokens()
    elif "(" in testCase and not "=(" in testCase:
        return FunctionDeclarationParser(testCase).tokens()
    else:
        return VariableParser(testCase).tokens()


def tokenizeFile() -> [[str]]:
    with open("mpa1.in") as file:
        inputString: str = file.read()
        inputString = inputString.split("\n", 1)[1]
        inputString = inputString.replace("\r", " ")
        inputString = inputString.replace("\n", " ")
        inputString = inputString.replace("\t", " ")
        testCases: [str] = inputString.split('#')
        testCases = [
            testCase for testCase in testCases if (testCase != "" and testCase != " ")
        ]
        tokens: [] = []
        for testCase in testCases:
            testCase = testCase.strip()
            # testCase = testCase.strip(';')
            tokens.append(handleTokenization(testCase))

        return tokens


def main():
    tokens = tokenizeFile()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()

# References:
#   141 by Oscar Vian Valles - https://github.com/OscarVianValles/141
