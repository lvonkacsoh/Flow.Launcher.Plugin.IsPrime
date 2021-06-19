# encoding=utf8
from flowlauncher import FlowLauncher


class Main(FlowLauncher):

    DISPLAYED_FACTOR_LIMIT = 11  # has to be a prime, it's the law >:(
    DIVISOR_LIST_SHORTENER = ".."
    PLACEHOLDER_NUMBER = "X"
    MSG_ARG_IS_NAN = "Floating point numbers like 17.42 are not valid. Texts are right out. Duh."
    MSG_ARG_IS_NEGATIVE = "Why even bother adding the minus? Just check the positive value."
    MSG_IS_PRIME = "{} is a prime.".format(PLACEHOLDER_NUMBER)
    MSG_IS_NO_PRIME = "{} is not a prime.".format(PLACEHOLDER_NUMBER)
    MSG_NUMBER_EVEN = "Because it's an even number."
    MSG_NUMBER_DIVISABLE_BY = "Because it can be divided by {}.".format(
        PLACEHOLDER_NUMBER)
    LOW_PRIME_THRESHOLD = 3  # 1-3 are primes so don't check those

    messages = []

    def addMessage(self, title, subTitle=None, img="failure"):
        self.messages.append({
            "Title": title,
            "SubTitle": subTitle,
            "IcoPath": "assets/{}.png".format(img),
        })

    def isPrime(self, number: int):
        if number > self.LOW_PRIME_THRESHOLD:
            if number % 2 == 0:
                return {"isPrime": False, "message": self.MSG_NUMBER_EVEN}
            factors = self.getFactors(number)
            if len(factors) > 0:
                return {
                    "isPrime": False,
                    "message": self.MSG_NUMBER_DIVISABLE_BY.replace(
                        self.PLACEHOLDER_NUMBER,
                        ", ".join(map(str, factors))
                    )
                }
        # number < 4 or no divisors found
        return {"isPrime": True, "message": None}

    def shortenList(self, lst: list) -> list:
        if len(lst) >= self.DISPLAYED_FACTOR_LIMIT:
            shortenedList = lst[:self.DISPLAYED_FACTOR_LIMIT]
            shortenedList.append(self.DIVISOR_LIST_SHORTENER)
            return shortenedList
        return lst

    def getFactors(self, number: int) -> list:
        factors = set()
        # start at 3 and only check odd numbers up to sqrt(n)+1
        for i in range(self.LOW_PRIME_THRESHOLD, int(number**0.5) + 1, 2):
            if number % i == 0:
                factors.add(i)
                factors.add(number//i)
        asList = list(factors)
        asList.sort()
        return self.shortenList(asList)

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
                if value < 0:
                    title = "Error: Given number musn't be negative!"
                    subTitle = self.MSG_ARG_IS_NEGATIVE
                    img = "failure"
                elif value == 0:
                    title = "You have summoned a black hole - congratulations!"
                    subTitle = "By doing so you have doomed us all. I hope you're proud."
                    img = "black-hole"
                else:
                    result = self.isPrime(value)
                    title = self.MSG_IS_PRIME if result["isPrime"] else self.MSG_IS_NO_PRIME
                    title = title.replace(self.PLACEHOLDER_NUMBER, str(value))
                    subTitle = result["message"]
                    img = "success" if result["isPrime"] else "failure"
            else:
                title = "Error: [ {} ]  is not an integer!".format(value)
                subTitle = self.MSG_ARG_IS_NAN
                img = "failure"

            self.addMessage(title, subTitle, img)

        return self.messages
