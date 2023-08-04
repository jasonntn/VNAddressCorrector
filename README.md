# VNAddressCorrector

Correct name of 3 level division: ward (Phường/Xã), district (Quận/Huyện), province(Tỉnh/Thành Phố) in Vietnam address.

## Installation
```bash
pip install vnac
```
## Usage
```python
>>> from vnac.corrector import AddressCorrector
>>> # Address must be in string format "..., {ward}, {district}, {province}" (split by ',')
>>> address = "Số 36A Đường 29, Ấp Tân Tiến, Tân Thìng Hội, Củ Chí, HCM"
>>> corrector = AddressCorrector()
>>> corrected = corrector.correct(address)
>>> corrected
Address(country=None, province=Division(name='HCM', code=79), district=Division(name='Củ Chi', code=None), ward=Division(name='Tân Thông Hội', code=None), street=Division(name='Số 36A Đường 29, Ấp Tân Tiến', code=None))
>>>str(corrected)
"Số 36A Đường 29, Ấp Tân Tiến, Tân Thông Hội, Củ Chi, HCM"
```
