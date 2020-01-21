
# def functionDefinitionParser(testCase) -> [str]:


def hasDataType(line):
    if "double" in line or "int" in line or "char" in line or "float" in line or "void" in line:
        return True
    else:
        return False


def functionDeclarationParser(testCase) -> [str]:
    tokenized: [str] = testCase.split(" ", 1)
    name: str = tokenized[1]
    tokenized.pop()

    splitName: [str] = name.split("\n", 1)

    print(splitName)

    tokenized.append(splitName[0])

    if len(splitName) > 1:
        for x in variableParser(splitName[1]):
            tokenized.append(x)

    return tokenized


def variableParser(testCase) -> [str]:
    tokenized: [str] = testCase.split(" ", 1)
    variables: str = tokenized[1]

    # print(variables)

    tokenized.pop()

    for temp in variables.split(","):
        if hasDataType(temp):
            for item in temp.split(" "):
                if item != "":
                    tokenized.append(item)
        elif "\n" in temp:
            tempList = temp.split("\n")
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

    # print(tokenized)

    return tokenized


def handleParsing(testCase) -> [str]:
    if "{" in testCase:
        return [testCase]
    elif "(" in testCase:
        return functionDeclarationParser(testCase)
    else:
        return variableParser(testCase)


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
            testCase = testCase.strip(';')
            parsed.append(handleParsing(testCase))

        return parsed


def main():
    tokenizeFile()


if __name__ == "__main__":
    main()
