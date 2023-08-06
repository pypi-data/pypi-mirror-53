import re


EOL = re.compile(rb'[\r\n]')
NON_EOL = re.compile(rb'[^\r\n]')

WHITE_SPACE = re.compile(rb'[\x00\t\n\f\r ]')
NON_SPACE = re.compile(rb'[^\x00\t\n\f\r ]')

DELIMITER = re.compile(rb'[()<>\[\]{}/%]')

REGULAR = re.compile(rb'[^\x00\t\n\f\r ()<>\[\]{}/%]')
NON_REGULAR = re.compile(rb'[\x00\t\n\f\r ()<>\[\]{}/%]')

NUMBER = re.compile(rb'[0-9]')
NON_NUMBER = re.compile(rb'[^0-9]')

STRING = re.compile(rb'[^()]')
NON_STRING = re.compile(rb'[()\\]')

HEX_STRING = re.compile(rb'[0-9a-fA-F]')
NON_HEX_STRING = re.compile(rb'[^\x00\t\n\f\r 0-9a-fA-F]')

NON_KEYWORD = re.compile(br'[\x00\t\n\f\r #/%\[\]()<>{}]')
