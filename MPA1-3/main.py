from abc import ABC, abstractmethod


def hasDataType(line) -> bool:
    if "double" in line or "int" in line or "char" in line or "float" in line or "void" in line or "return" in line:
        return True
    else:
        return False


def hasOperation(line) -> bool:
    if "+" in line or "*" in line or "/" in line or "-" in line:
        return True
    else:
        return False


def hasSucceedingDataTypes(tokens) -> bool:
    pos: int = 0
    for token in tokens:
        if hasDataType(token) and pos + 1 < len(tokens):
            if hasDataType(tokens[pos + 1]):
                return True
        pos += 1
    return False

def hasMultipleDataTypes(tokens) -> bool:
    count = 0
    for token in tokens:
        if hasDataType(token):
            count += 1

    return True if count > 1 else False


def hasDuplicateVar(tokens) -> bool:
    variables = []
    for token in tokens:
        if "=" in token:
            variables.append(token.split("=")[0])
        elif not hasDataType(token):
            variables.append(token)
    if len(variables) == len(set(variables)):
        return False
    else:
        return True


def hasUndeclaredVar(tokens) -> bool:
    variables = []
    values = []
    for token in tokens:
        if "=" in token:
            temp = token.split("=")
            variables.append(temp[0])
            if not temp[1].replace('.', '').isdigit() and "'" not in temp[1]:
                values.append(temp[1])
            # checks if there is an empty character declared
            elif "''" in temp[1]:
                return True
            else:
                # we add an empty element so that we could save the position of the values
                values.append(' ')
        elif not hasDataType(token) and not ";":
            variables.append(token)
            # we add an empty element so that we could save the position of the values
            values.append(' ')
    # creates temporary list to remove empty elements
    temp = []
    for x in values:
        temp.append(x)

    # removes empty elements
    for item in temp:
        if ' ' in item:
            temp.remove(' ')
    if ' ' in temp:
        temp.remove(' ')

    if len(temp) > 0:
        if any(x in values for x in variables):
            valuePos = 0
            varPos = 0
            for i in values:
                for j in variables:
                    if i == j:
                        # if the variable was assigned to another variable before it was declared, it returns True
                        return False if valuePos < varPos else True
                    varPos += 1
                valuePos += 1
        else:
            return True
    else:
        return False


def usedUndeclaredVar(tokens) -> bool:
    variables = []
    used = []
    pos: int = 0
    for token in tokens:
        if hasDataType(token) and not hasDataType(tokens[pos + 1]):
            variables.append(tokens[pos + 1].split("=")[0])
        pos += 1
    for token in tokens:
        if "=" in token:
            temp = token.split("=")[1]
            for t in temp:
                if not hasOperation(t) and not t.isnumeric():
                    used.append(t)
    for u in used:
        pos = 0
        for v in variables:
            if u == v:
                break
            pos += 1
        if pos == len(variables):
            return True

    return False

def hasMultipleDeclarations(tokens) -> str:
    pos: int = 0
    variables: [str] = []

    for token in tokens:
        if hasDataType(token) and not hasDataType(tokens[pos+1]):
            variables.append(tokens[pos+1].split("=")[0])
        pos += 1

    if len(variables) == len(set(variables)):
        return False
    else:
        return True


def findDataType(tokens, variable) -> str:
    pos: int = 0
    for token in tokens:
        if token == variable:
            return tokens[pos - 1]
        pos += 1
    return "none"


def isDeclared(tokens, variable) -> bool:
    pos: int = 0
    for token in tokens:
        if token.split("=")[0] == variable:
            if hasDataType(tokens[pos - 1]):
                return True
        pos += 1
    return False


class Parser(ABC):
    @abstractmethod
    def tokenize(self):
        pass

    @abstractmethod
    def check(self):
        pass


class VariableParser(Parser):
    def __init__(self, testCase: str):
        self._string: str = testCase
        self._tokens: [str] = []
        self._validity: bool = True
        self.tokenize()
        self.check()

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
            elif ";" in temp:
                temp = temp.replace(" ", "")
                self._tokens.append(temp.split(";")[0])
                self._tokens.append(";")
            else:
                # removes the spaces
                temp = temp.replace(" ", "")
                self._tokens.append(temp)

    def check(self):
        if ";" not in self._tokens:
            self._validity = False
            return
        # if the variable declaration uses the same variable more than once
        elif hasDuplicateVar(self._tokens):
            self._validity = False
            return
        # if there was an undeclared variable used
        elif hasUndeclaredVar(self._tokens):
            self._validity = False
            return

        prev = ""
        for token in self._tokens:
            if prev != "":
                # if two data types were used in succession
                if hasDataType(token) and hasDataType(prev):
                    self._validity = False
                    return
                elif hasDataType(token) and ";" not in prev:
                    self._validity = False
                    return
                elif hasMultipleDataTypes(token):
                    self._validity = False
                    return
            prev = token

    def tokens(self) -> [str]:
        return self._tokens

    def validity(self) -> str:
        return "Valid Variable Declaration" if self._validity == True else "Invalid Variable Declaration"


class FunctionDeclarationParser(Parser):
    def __init__(self, testCase: str):
        self._string: str = testCase
        self._name: [str] = []
        self._params: [str] = []
        self._validity: bool = True
        self.tokenize()
        self.check()

    def tokenize(self):
        # makes a list containing the data type at index 0 and everything else at index 1
        self._name: [str] = self._string.split(" ", 1)
        # since the name is stored somewhere in index 1, we store it in a variable
        trail: str = self._name[1]
        # we remove the last item of the list which was everything to the right of the data type
        self._name.pop()

        # checks if another function declaration is found
        if '),' in trail:
            # splits the list using ),
            comma: [str] = trail.split('),')
            for item in comma:
                # returns the parenthesis that we removed during split
                if item != comma[-1]:
                    item += ')'
                # we try to isolate the name of the function by splitting the trail with the first close parenthesis we see
                temp: [str] = item.split(")", 1)
                # currently the list looks like this: [function name with parameters, everything else]

                hasSemiColon = False
                if ";" in temp:
                    hasSemiColon = True

                # removes everything after the ) from the list
                temp.pop()

                # appends function name while using the open parenthesis as the delimiter
                self._name.append(temp[0].split("(")[0])
                # appends list of function parameters while using the open parenthesis as the delimiter and stripping the close parenthesis at the end
                self._params = VariableParser(
                    temp[0].split("(")[1].strip(")")).tokens()

                if hasSemiColon:
                    self._name.append(";")

        else:
            # we try to isolate the name of the function by splitting the trail with the first close parenthesis we see
            temp: [str] = trail.split(")", 1)
            # currently the list looks like this: [function name with parameters, everything else]

            hasSemiColon = False
            if ";" in temp:
                hasSemiColon = True

            # removes everything after the ) from the list
            temp.pop()

            # appends function name while using the open parenthesis as the delimiter
            self._name.append(temp[0].split("(")[0])
            # appends list of function parameters while using the open parenthesis as the delimiter and stripping the close parenthesis at the end
            self._params = VariableParser(
                temp[0].split("(")[1].strip(")")).tokens()

            if hasSemiColon:
                self._name.append(";")

    def check(self):
        prev = ""
        if ";" not in self._name:
            self._validity = False
            return

        for token in self._name:
            if prev != "":
                # if two data types were used in succession
                if hasDataType(token) and hasDataType(prev):
                    self._validity = False
                    return
            prev = token

        for param in self._params:
            if "=" in param:
                self._validity = False
                return

        # if the variable declaration uses the same variable more than once
        if hasDuplicateVar(self._params):
            self._validity = False
            return
        # if there was an undeclared variable used
        elif hasUndeclaredVar(self._params):
            self._validity = False
            return
    
    def name(self):
        return self._name

    def params(self):
        return self._params

    def validity(self) -> str:
        return "Valid Function Declaration" if self._validity == True else "Invalid Function Declaration"

    def valid(self) -> str:
        return self._validity


class FunctionDefinitionParser(Parser):
    def __init__(self, testCase: str):
        self._string: str = testCase
        self._name: [str] = []
        self._params: [str] = []
        self._operations: [str] = []
        self._return: [str] = []
        self._validity: bool = True
        self.tokenize()
        if self._validity == True:
            self.check()

    def tokenize(self):
        # creates a list with the function name in index 0 and everything else at index 1
        self._tokens: str = self._string.split("{", 1)
        trail: str = self._tokens[1].strip()
        trail = trail.strip("}")
        self._tokens.pop()
        # we use the tokenize function from the function declaration class
        functionDeclaration = FunctionDeclarationParser(self._tokens[0] + ';')
        functionDeclaration.check()
        if functionDeclaration.valid() == False:
            self._validity = False
            return
        self._name = functionDeclaration.name()
        self._params = functionDeclaration.params()
        lines: [str] = trail.split(";")
        lines.pop()
        for line in lines:
            if "{" in line.strip() or "}" in line.strip():
                self._validity = False
                return
            # we use the tokenize function from the variable class
            variable = VariableParser(line.strip())
            if "return" in variable.tokens():
                self._return = variable.tokens()
            else:
                for item in variable.tokens():
                    self._operations.append(item)

    def check(self):
        temp: [str] = []

        for param in self._params:
            if param != '':
                temp.append(param)
        for operation in self._operations:
            if operation != '':
                temp.append(operation)

        # if function type is void and has a return value
        if self._name[0] == "void" and len(self._return) > 0:
            self._validity = False
            return
        # if a variable was declared multiple times
        elif hasMultipleDeclarations(temp):
            self._validity = False
            return
        # if return type is not the same as function type
        elif len(self._return) > 0 and findDataType(temp, self._return[1]) != self._name[0] and findDataType(temp, self._return[1]) != "none":
            self._validity = False
            return
        # if the return variable was not declared
        elif len(self._return) > 0 and not hasOperation(self._return[1]) and not isDeclared(temp, self._return[1]):
            self._validity = False
            return
        # if the parameters have succeeding data types
        elif hasSucceedingDataTypes(self._params):
            self._validity = False
            return
        # if params only has one token and is a data type
        elif len(self._params) == 1:
            if hasDataType(self._params[0]):
                self._validity = False
                return
        # if the functions uses an undeclared variable
        elif usedUndeclaredVar(temp):
            self._validity = False
            return

    def tokens(self) -> [str]:
        return self._tokens

    def validity(self) -> str:
        return "Valid Function Definition" if self._validity == True else "Invalid Function Definition"


def handleChecks(testCase) -> [str]:
    if "{" in testCase:
        return FunctionDefinitionParser(testCase).validity()
    elif "(" in testCase and not "=(" in testCase:
        return FunctionDeclarationParser(testCase).validity()
    else:
        return VariableParser(testCase).validity()


def parseFile() -> [[str]]:
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
        cases: [] = []
        for testCase in testCases:
            testCase = testCase.strip()
            cases.append(handleChecks(testCase))

        return cases


def main():
    file = open("po1.out", "w+")
    cases = parseFile()
    for case in cases:
        file.write(case)
        file.write("\n")
    file.close()


if __name__ == "__main__":
    main()


# References:
#   141 by Oscar Vian Valles - https://github.com/OscarVianValles/141
#   How to check if one of the following items is in a list? - https://stackoverflow.com/questions/740287/how-to-check-if-one-of-the-following-items-is-in-a-list
#   Python : 3 ways to check if there are duplicates in a List - https://thispointer.com/python-3-ways-to-check-if-there-are-duplicates-in-a-list/
#   Python String isnumeric() and its application - https://www.geeksforgeeks.org/python-string-isnumeric-application/
#   Iterating each character in a string using Python - https://stackoverflow.com/questions/538346/iterating-each-character-in-a-string-using-python
