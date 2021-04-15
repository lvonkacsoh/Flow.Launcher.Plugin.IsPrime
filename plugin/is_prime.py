# encoding=utf8
from flowlauncher import FlowLauncher


class Main(FlowLauncher):
    def isPrime(self, number):
        if number % 2 == 0:
            return False
        # start at 3 and only check odd number up to sqrt(n)+1
        for i in range(3, int(number**0.5)+1, 2):
            if number % i == 0:
                return False
        return True

    def getNumberValue(self, text):
        try:
            return (True, int(text))
        except ValueError:
            return (False, text)

    # part of the FlowLauncher lifecycle, 'key' is a single string of whatever you type after "isPrime "
    def query(self, key):
        if len(key) == 0:
            return

        results = []
        numbers = key.split(" ")
        for number in numbers:
            subTitle = ""
            isNumber, value = self.getNumberValue(number)
            if isNumber:
                isPrime = self.isPrime(value)
                title = "{} is {}a prime.".format(
                    value, "" if isPrime else "not ")
                img = "success" if isPrime else "failure"
            else:
                title = "ERROR: \"{}\" is not an integer!".format(value)
                subTitle = "Note: Floating point numbers like 17.42 are not valid. Texts are right out. Duh."
                img = "failure"
            # these are the items which are finally shown in the result list
            results.append({
                "Title": title,
                "SubTitle": subTitle,
                "IcoPath": "assets/{}.png".format(img),
                "JsonRPCAction": {  # actually no clue what this is, leaving it in for now..
                    "dontHideAfterAction": True
                }
            })

        return results
