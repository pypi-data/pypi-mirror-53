#  This file is part of TALER
#  (C) 2017, 2019 Taler Systems SA
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later
#  version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA  02110-1301  USA
#
#  @author Marcello Stanisci
#  @version 0.1
#  @repository https://git.taler.net/taler-util.git/


##
# Exception class to raise when an operation between two
# amounts of different currency is being attempted.
class CurrencyMismatch(Exception):
    hint = "Client gave amount with unsupported currency."
    http_status_code = 406

    ##
    # Init constructor.
    #
    # @param self the object itself.
    # @param curr1 first currency involved in the operation.
    # @param curr2 second currency involved in the operation.
    def __init__(self, curr1, curr2) -> None:
        super(CurrencyMismatch, self).__init__("%s vs %s" % (curr1, curr2))


##
# Exception class to raise when a amount string is not valid.
class BadFormatAmount(Exception):

    hint = "Malformed amount string"

    ##
    # Init constructor.
    #
    # @param self the object itself.
    # @param faulty_str the invalid amount string.
    def __init__(self, faulty_str) -> None:
        super(BadFormatAmount,
              self).__init__("Bad format amount: " + faulty_str)


##
# Main Amount class.
class NumberTooBig(Exception):
    hint = "Number given is too big"

    def __init__(self) -> None:
        super(NumberTooBig, self).__init__("Number given is too big")


class NegativeNumber(Exception):
    hint = "Negative number given as value and/or fraction"

    def __init__(self) -> None:
        super(NegativeNumber,
              self).__init__("Negative number given as value and/or fraction")


class Amount:
    ##
    # How many "fraction" units make one "value" unit of currency
    # (Taler requires 10^8).  Do not change this 'constant'.
    @staticmethod
    def _fraction() -> int:
        return 10**8

    ##
    # Max value admitted: 2^53 - 1.  This constant is dictated
    # by the wallet: JavaScript does not go beyond this value.
    @staticmethod
    def _max_value() -> int:
        return (2**53) - 1

    ##
    # Init constructor.
    #
    # @param self the object itself.
    # @param currency the amount's currency.
    # @param value integer part the amount
    # @param fraction fractional part of the amount
    def __init__(self, currency, value=0, fraction=0) -> None:
        if value < 0 or fraction < 0:
            raise NegativeNumber()
        self.value = value
        self.fraction = fraction
        self.currency = currency
        self.__normalize()
        if self.value > Amount._max_value():
            raise NumberTooBig()

    ##
    # Normalize amount.  It means it makes sure that the
    # fractional part is less than one unit, and transfers
    # the overhead to the integer part.
    def __normalize(self) -> None:
        if self.fraction >= Amount._fraction():
            self.value += int(self.fraction / Amount._fraction())
            self.fraction = self.fraction % Amount._fraction()

    ##
    # Parse a string matching the format "A:B.C",
    # instantiating an amount object.
    #
    # @param cls unused.
    # @param amount_str the stringified amount to parse.
    @classmethod
    def parse(cls, amount_str: str):
        exp = r'^\s*([-_*A-Za-z0-9]+):([0-9]+)\.?([0-9]+)?\s*$'
        import re
        parsed = re.search(exp, amount_str)
        if not parsed:
            raise BadFormatAmount(amount_str)

        ##
        # Checks if the input overflows.
        #
        # @param arg the input number to check.
        # @return True if the overflow occurs, False otherwise.
        def check_overflow(arg):
            # Comes from 2^53 - 1
            JAVASCRIPT_MAX_INT = "9007199254740991"
            if len(JAVASCRIPT_MAX_INT) < len(arg):
                return True
            if len(JAVASCRIPT_MAX_INT) == len(arg):
                # Assume current system can afford to store
                # a number as big as JAVASCRIPT_MAX_INT.
                tmp = int(arg)
                tmp_js = int(JAVASCRIPT_MAX_INT)

                if tmp > tmp_js - 1:  # - 1 leaves room for the fractional part
                    return True
            return False

        if check_overflow(parsed.group(2)):
            raise AmountOverflow("integer part")

        value = int(parsed.group(2))
        fraction = 0
        for i, digit in enumerate(parsed.group(3) or "0"):
            fraction += int(int(digit) * (Amount._fraction() / 10**(i + 1)))
            if check_overflow(str(fraction)):
                raise AmountOverflow("fraction")

        return cls(parsed.group(1), value, fraction)

    ##
    # Compare two amounts.
    #
    # @param am1 first amount to compare.
    # @param am2 second amount to compare.
    # @return -1 if a < b
    #          0 if a == b
    #          1 if a > b
    @staticmethod
    def cmp(am1, am2) -> int:
        if am1.currency != am2.currency:
            raise CurrencyMismatch(am1.currency, am2.currency)
        if am1.value == am2.value:
            if am1.fraction < am2.fraction:
                return -1
            if am1.fraction > am2.fraction:
                return 1
            return 0
        if am1.value < am2.value:
            return -1
        return 1

    ##
    # Setter method for the current object.
    #
    # @param self the object itself.
    # @param currency the currency to set.
    # @param value the value to set.
    # @param fraction the fraction to set.
    def set(self, currency: str, value=0, fraction=0) -> None:
        self.currency = currency
        self.value = value
        self.fraction = fraction

    ##
    # Add the given amount to this one.
    #
    # @param self the object itself.
    # @param amount the amount to add to this one.
    def add(self, amount) -> None:
        if self.currency != amount.currency:
            raise CurrencyMismatch(self.currency, amount.currency)
        self.value += amount.value
        self.fraction += amount.fraction
        self.__normalize()

    ##
    # Subtract amount from this one.
    #
    # @param self this object.
    # @param amount the amount to subtract to this one.
    def subtract(self, amount) -> None:
        if self.currency != amount.currency:
            raise CurrencyMismatch(self.currency, amount.currency)
        if self.fraction < amount.fraction:
            self.fraction += Amount._fraction()
            self.value -= 1
        if self.value < amount.value:
            raise ValueError('self is lesser than amount to be subtracted')
        self.value -= amount.value
        self.fraction -= amount.fraction

    ##
    # Convert the amount to a string.
    #
    # @param self this object.
    # @param ndigits how many digits we want for the fractional part.
    # @param pretty if True, put the currency in the last position and
    #        omit the colon.
    def stringify(self, ndigits=0, pretty=False) -> str:
        s = str(self.value)
        if self.fraction != 0:
            s += "."
            frac = self.fraction
            while frac != 0 or ndigits != 0:
                s += str(int(frac / (Amount._fraction() / 10)))
                frac = (frac * 10) % (Amount._fraction())
                ndigits -= 1
        elif ndigits != 0:
            s += "." + ("0" * ndigits)
        if not pretty:
            return f"{self.currency}:{s}"
        return f"{s} {self.currency}"

    ##
    # Dump the Taler-compliant 'dict' amount from
    # this object.
    #
    # @param self this object.
    def dump(self) -> dict:
        return dict(
            value=self.value, fraction=self.fraction, currency=self.currency
        )
