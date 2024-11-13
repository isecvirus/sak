# Privacy


---

## [mask](mask)

### Simple usage
```python
from privacy.mask import Mask
from privacy.mask.rules import Email

string = "Contact me on virus@github.com"

mask = Mask(string, rules=[Email()])
masked_string = mask.mask() # Contact me on *****@******.***
```

## `Mask` parameters
| Parameter |  Type  | Required | Default |
|:---------:|:------:|:--------:|:-------:|
|  string   | `str`  |    ✅    |
|   rules   | `Rule` |    ✅    |

## `Mask` methods
|  method  | return type | parameters |
|:--------:|:-----------:|:----------:|
| `mask()` |    `str`    |            |

## 🛠️ Creating custom rules
```python
from privacy.mask import Rule

class RuleName(Rule):
    """
    The following parameters aren't required, but they are in the parent class 'Rule' (so implement them if needed):
    
       wildcard - The replacement character for the sensitive data (default='*')
          limit - The limit of the masked information (default=None for unlimited)
    placeholder - A full information replacement instead of the wildcard
    """
    
    def __init__(self, wildcard:str='*', limit: int = None, placeholder:str=None):
        super().__init__(wildcard=wildcard, limit=limit, placeholder=placeholder)

    def apply(self, string: str) -> str:
        # Implement your rule here
        pass
```

###### Example:
```python
from privacy.mask import Rule
from privacy.mask import Mask
import re

class Numbers(Rule):
    """ Masking all numbers in the whole string """
    def full_length(self, match):
        return self.wildcard * len(match.group())

    def apply(self, string:str):
        return re.sub(r'\d+', self.full_length, string)

string = "Numbers from 100 to 99999"
mask = Mask(string, [Numbers()])
masked_string = mask.mask()
```

---
