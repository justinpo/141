def hasDataType(line) -> bool:
    if "double" in line or "int" in line or "char" in line or "float" in line or "void" in line or "return" in line:
        return True
    else:
        return False

def variableTokenizer(testCase) -> [str]:
    tokenized: [str] = testCase.split(" ", 1)
    
    if len(tokenized) > 1:
        trail: str = tokenized[1]
    else:
        trail: str = tokenized[0]

    tokenized.pop()

    for temp in trail.split(","):
        if hasDataType(temp):
            for item in temp.split(" "):
                if item != "":
                    tokenized.append(item)
        elif "\n" in temp:
            tempList: [str] = temp.split("\n")
            for item in tempList:
                if " " in item:
                    for item in item.split(" "):
                        tokenized.append(item)
                elif item != "":
                    item = item.replace(" ", "")
                    tokenized.append(item)
        else:
            temp = temp.replace(" ", "")
            tokenized.append(temp)

    return tokenized


def functionDeclarationTokenizer(testCase) -> [str]:
    # makes a list containing the data type at index 0 and everything else at index 1
    tokenized: [str] = testCase.split(" ", 1)
    # since the name is stored somewhere in index 1, we store it in a variable
    trail: str = tokenized[1]
    # we remove the last item of the list which was everything to the right of the data type
    tokenized.pop()

    # we try to isolate the name of the function by splitting the trail with the first close parenthesis we see
    temp: [str] = trail.split(")", 1)
    # currently the list looks like this: [function name with parameters, everything else]

    # removes everything after the ) from the list
    temp.pop()

    # appends function name while using the open parenthesis as the delimiter
    tokenized.append(temp[0].split("(")[0])
    # appends list of function parameters while using the open parenthesis as the delimiter and stripping the close parenthesis at the end
    tokenized.append(variableTokenizer(temp[0].split("(")[1].strip(")")))

    # checks if the list for isolating the name contains anything other than the name and parameters
    # if len(temp) > 1:
    #     for x in variableTokenizer(temp[1]):
    #         tokenized.append(x)

    return tokenized


def functionDefinitionTokenizer(testCase) -> [str]:
    tokenized: str = testCase.split("{", 1)
    trail: str = tokenized[1].strip()
    trail = trail.strip("}")
    tokenized.pop()

    tokenized = functionDeclarationTokenizer(tokenized[0])
    lines: [str] = trail.split(";")
    lines.pop()
    operations: [str] = []
    for line in lines:
        for item in variableTokenizer(line.strip()):
            operations.append(item)
        
    tokenized.append(operations) 

    return tokenized


def handleTokenization(testCase) -> [str]:
    if "{" in testCase:
        return functionDefinitionTokenizer(testCase)
    elif "(" in testCase:
        return functionDeclarationTokenizer(testCase)
    else:
        return variableTokenizer(testCase)


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
        parsed: [] = []
        for testCase in testCases:
            testCase = testCase.strip()
            # testCase = testCase.strip(';')
            parsed.append(handleTokenization(testCase))

        return parsed


def main():
    parsed = tokenizeFile()
    for item in parsed:
        print(item)


if __name__ == "__main__":
    main()
