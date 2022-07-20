# encoding=utf8
from flowlauncher import FlowLauncher


class MessageDTO:
    def __init__(self, title: str, subtitle: str, image: str) -> None:
        self.title = title
        self.subtitle = subtitle
        self.image = image

    def asFlowMessage(self) -> dict:
        return {
            "Title": self.title,
            "SubTitle": self.subtitle,
            "IcoPath": "assets/{}.png".format(self.image),
        }


class Main(FlowLauncher):
    DISPLAYED_FACTOR_LIMIT = 11  # has to be a prime, it's the law >:(
    FACTOR_LIST_SHORTENER = ".."
    PLACEHOLDER_NUMBER = "X"
    MSG_IS_PRIME = "{} is a prime.".format(PLACEHOLDER_NUMBER)
    MSG_IS_NO_PRIME = "{} is not a prime.".format(PLACEHOLDER_NUMBER)
    MSG_NUMBER_DIVISABLE_BY = "Because it can be divided by {}.".format(PLACEHOLDER_NUMBER)
    LOW_PRIME_THRESHOLD = 3  # start at 3 since 1 and 2 are edgecases
    IMG_FAILURE = "failure"

    messages = []

    def addMessage(self, message: MessageDTO):
        self.messages.append(message.asFlowMessage())

    def shortenList(self, lst: list) -> list:
        if len(lst) >= self.DISPLAYED_FACTOR_LIMIT:
            shortenedList = lst[:self.DISPLAYED_FACTOR_LIMIT]
            shortenedList.append(self.FACTOR_LIST_SHORTENER)
            return shortenedList
        return lst

    def calculateFactors(self, number: int) -> list:
        factors = set()
        # only check odd numbers up to sqrt(n)+1
        for i in range(self.LOW_PRIME_THRESHOLD, int(number**0.5) + 1, 2):
            if number % i == 0:
                factors.add(i)
                factors.add(number//i)
        asList = list(factors)
        asList.sort()
        return self.shortenList(asList)

    def tryToParseValueAsNumber(self, text: str):
        try:
            return (True, int(text))
        except ValueError:
            return (False, text)

    def checkNumberForEdgecase(self, number: int) -> tuple:
        isEdgecase = True
        title = ""
        subtitle = ""
        img = self.IMG_FAILURE

        if number < 0:
            title = "Error: Given number musn't be negative!"
            subtitle = "Why even bother adding the minus? Just check the positive value."
        elif number == 0:
            title = "You have summoned a black hole - congratulations!"
            subtitle = "By doing so you have doomed us all. I hope you're proud."
            img = "black-hole"
        elif number == 1:
            title = self.MSG_IS_NO_PRIME.replace(
                self.PLACEHOLDER_NUMBER, str(number))
            subtitle = "One is special but not considered a prime."
        elif number > 2 and number % 2 == 0:
            title = self.MSG_IS_NO_PRIME.replace(
                self.PLACEHOLDER_NUMBER, str(number))
            subtitle = "Because it's an even number."
        else:
            isEdgecase = False

        return isEdgecase, MessageDTO(title, subtitle, img)

    def isPrime(self, number: int) -> MessageDTO:
        isEdgecase, edgecaseData = self.checkNumberForEdgecase(number)
        if isEdgecase:
            return edgecaseData

        factors = self.calculateFactors(number)
        hasFactors = len(factors) > 0

        if hasFactors:
            title = self.MSG_IS_NO_PRIME
            subtitle = self.MSG_NUMBER_DIVISABLE_BY.replace(
                self.PLACEHOLDER_NUMBER,
                ", ".join(map(str, factors))
            )
            img = self.IMG_FAILURE
        else:
            title = self.MSG_IS_PRIME
            subtitle = ""
            img = "success"
        title = title.replace(self.PLACEHOLDER_NUMBER, str(number))

        return MessageDTO(title, subtitle, img)

    def query(self, arguments: str) -> list:
        args = arguments.strip()
        if len(args) == 0:
            return

        for number in args.split(" "):
            isNumber, value = self.tryToParseValueAsNumber(number)
            message = None

            if isNumber:
                message = self.isPrime(value)
            else:
                title = "Error:  [ {} ]  is not an integer!".format(value)
                subtitle = "Floating point numbers like 17.42 are not valid. Texts are right out. Duh."
                img = self.IMG_FAILURE
                message = MessageDTO(title, subtitle, img)

            self.addMessage(message)

        return self.messages
