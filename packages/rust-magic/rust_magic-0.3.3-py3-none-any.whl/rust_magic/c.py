string = '[US1] Evaluate any matters identified when testing segment information.[US2]'
import re
print(re.findall(r'\[[^]]*\]', string)[-1])
