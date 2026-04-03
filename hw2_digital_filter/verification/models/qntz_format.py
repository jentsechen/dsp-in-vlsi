from dataclasses import dataclass, field


@dataclass
class QntzFormat:
    fix_en: bool = False
    int_bit: int = 15
    frac_bit: int = 16

    def total_bit_width(self):
        return 1 + self.int_bit + self.frac_bit


@dataclass
class QntzFormatSet:
    input: QntzFormat = field(default_factory=QntzFormat)
    coef: QntzFormat = field(default_factory=QntzFormat)
    mult: QntzFormat = field(default_factory=QntzFormat)
    add: QntzFormat = field(default_factory=QntzFormat)