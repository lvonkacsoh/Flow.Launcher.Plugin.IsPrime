# encoding=utf8
from flowlauncher import FlowLauncher


class Main(FlowLauncher):
    PLACEHOLDER_NUMBER = "X"
    MSG_IS_PRIME = "{} is a prime".format(PLACEHOLDER_NUMBER)
    MSG_IS_NO_PRIME = "{} is not a prime".format(PLACEHOLDER_NUMBER)
    MSG_NUMBER_EVEN = "Because it's an even number."
    MSG_NUMBER_DIVISABLE_BY = "Because it can be devided by [{}]".format(
        PLACEHOLDER_NUMBER)

    messages = []

    def addMessage(self, title, subTitle=None, img="failure"):
        self.messages.append({
            "Title": title,
            "SubTitle": subTitle,
            "IcoPath": "assets/{}.png".format(img),
        })

    def isPrime(self, number: int):
        if number % 2 == 0:
            return {"isPrime": False, "message": self.MSG_NUMBER_EVEN}
        # start at 3 and only check odd number up to sqrt(n)+1
        for i in range(3, int(number**0.5)+1, 2):
            if number % i == 0:
                return {"isPrime": False, "message": self.MSG_NUMBER_DIVISABLE_BY.replace(self.PLACEHOLDER_NUMBER, str(i))}
        return {"isPrime": True, "message": None}

    def getNumberValue(self, text: str):
        try:
            return (True, int(text))
        except ValueError:
            return (False, text)

    def query(self, arguments: str):
        args = arguments.strip()
        if len(args) == 0:
            return

        for number in args.split(" "):
            subTitle = None
            isNumber, value = self.getNumberValue(number)

            if isNumber:
                result = self.isPrime(value)
                title = self.MSG_IS_PRIME if result["isPrime"] else self.MSG_IS_NO_PRIME
                title = title.replace(self.PLACEHOLDER_NUMBER, str(value))
                subTitle = result["message"]
                img = "success" if result["isPrime"] else "failure"
            else:
                title = "ERROR: \"{}\" is not an integer!".format(value)
                subTitle = "Note: Floating point numbers like 17.42 are not valid. Texts are right out. Duh."
                img = "failure"

            self.addMessage(title, subTitle, img)

        return self.messages
