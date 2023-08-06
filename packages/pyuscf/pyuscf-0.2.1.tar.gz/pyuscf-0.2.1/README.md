# pyuscf: USCF Member Service Area (MSA) for Python

The United States Chess Federation (USCF) website for publicly available
chess member information. The package is nothing more than a client, but there
are some limitations on searching for chess members' information.

Visit www.uschess.org for further information on the limitations.

## Usage

```python
>>> from pyuscf import Msa
>>> player = Msa(12743305)
>>> player.get_name()
'FABIANO CARUANA'
>>> player.get_regular_rating()
'2895* 2019-08-01'
>>> player.get_fide_rating()
'2818 2019-08-01'
>>>
```