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
#  @repository https://git.taler.net/copylib.git/
#  This code is "copylib", it is versioned under the Git repository
#  mentioned above, and it is meant to be manually copied into
#  any project which might need it.

class CurrencyMismatch(Exception):
    hint = "Internal logic error (currency mismatch)"
    http_status_code = 500
    def __init__(self, curr1, curr2) -> None:
        super(CurrencyMismatch, self).__init__(
            "%s vs %s" % (curr1, curr2))

class BadFormatAmount(Exception):
    hint = "Malformed amount string"
    def __init__(self, faulty_str) -> None:
        super(BadFormatAmount, self).__init__(
            "Bad format amount: " + faulty_str)

class NumberTooBig(Exception):
    hint = "Number given is too big"
    def __init__(self) -> None:
        super(NumberTooBig, self).__init__(
            "Number given is too big")

class NegativeNumber(Exception):
    hint = "Negative number given as value and/or fraction"
    def __init__(self) -> None:
        super(NegativeNumber, self).__init__(
            "Negative number given as value and/or fraction")

class Amount:
    # How many "fraction" units make one "value" unit of currency
    # (Taler requires 10^8).  Do not change this 'constant'.
    @staticmethod
    def _fraction() -> int:
        return 10 ** 8

    @staticmethod
    def _max_value() -> int:
        return (2 ** 53) - 1

    def __init__(self, currency, value=0, fraction=0) -> None:
        if value < 0 or fraction < 0:
            raise NegativeNumber()
        self.value = value
        self.fraction = fraction
        self.currency = currency
        self.__normalize()
        if self.value > Amount._max_value():
            raise NumberTooBig()

    # Normalize amount
    def __normalize(self) -> None:
        if self.fraction >= Amount._fraction():
            self.value += int(self.fraction / Amount._fraction())
            self.fraction = self.fraction % Amount._fraction()

    # Parse a string matching the format "A:B.C"
    # instantiating an amount object.
    @classmethod
    def parse(cls, amount_str: str):
        exp = r'^\s*([-_*A-Za-z0-9]+):([0-9]+)\.?([0-9]+)?\s*$'
        import re
        parsed = re.search(exp, amount_str)
        if not parsed:
            raise BadFormatAmount(amount_str)
        value = int(parsed.group(2))
        fraction = 0
        for i, digit in enumerate(parsed.group(3) or "0"):
            fraction += int(int(digit) * (Amount._fraction() / 10 ** (i+1)))
        return cls(parsed.group(1), value, fraction)

    # Comare two amounts, return:
    # -1 if a < b
    # 0 if a == b
    # 1 if a > b
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

    def set(self, currency: str, value=0, fraction=0) -> None:
        self.currency = currency
        self.value = value
        self.fraction = fraction

    # Add the given amount to this one
    def add(self, amount) -> None:
        if self.currency != amount.currency:
            raise CurrencyMismatch(self.currency, amount.currency)
        self.value += amount.value
        self.fraction += amount.fraction
        self.__normalize()

    # Subtract passed amount from this one
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

    # Dump string from this amount, will put 'ndigits' numbers
    # after the dot.
    def stringify(self, ndigits: int, pretty=False) -> str:
        if ndigits <= 0:
            raise BadFormatAmount("ndigits must be > 0")
        tmp = self.fraction
        fraction_str = ""
        while ndigits > 0:
            fraction_str += str(int(tmp / (Amount._fraction() / 10)))
            tmp = (tmp * 10) % (Amount._fraction())
            ndigits -= 1
        if not pretty:
            return "%s:%d.%s" % (self.currency, self.value, fraction_str)
        return "%d.%s %s" % (self.value, fraction_str, self.currency)

    # Dump the Taler-compliant 'dict' amount
    def dump(self) -> dict:
        return dict(value=self.value,
                    fraction=self.fraction,
                    currency=self.currency)
