from vnac.corrector import AddressCorrector

tests = [
    ("Nhi Bình, Châu Thanh, Tiền Giang", "Nhị Bình, Châu Thành, Tiền Giang", 82),
    ("Số 36A Đường 29, Ấp Tân Tiến, Tân Thìng Hội, Củ Chí, HCM", "Số 36A Đường 29, Ấp Tân Tiến, Tân Thông Hội, Củ Chi, HCM", 79),
    ("TP. Hô Ch Minh", "TP. Hồ Chí Minh", 79),
    ("Biên Hòa, Đng Nai", "Biên Hòa, Đồng Nai", 75),
    ("HẢI PHÒNG", "HẢI PHÒNG", 31),
    ("Nốt Bình, Châu Thơng, Biên Giang", "Nam Bình, Châu Thành, Kiên Giang", 91),
    ("Số 09 Hoàng Văn Thụ, Phường Tân An, TP.Buôn Ma Thuột, Tỉnh ĐắkLắk", "Số 09 Hoàng Văn Thụ, Phường Tân An, TP.Buôn Ma Thuột, Tỉnh Đắk Lắk", 66),
    ("Thôn Cây Sung, Xã DiênTân, Huyện Diên Khánh, Tỉnh Khánh Hòa", "Thôn Cây Sung, Xã Diên Tân, Huyện Diên Khánh, Tỉnh Khánh Hòa", 56),
    (
        "Thôn Cây Sung, Xã DiênTân, Huyện Diên Khánh, Tỉnh Khsasdfasdfjasoifdfaa",
        "Thôn Cây Sung, Xã Diên Tân, Huyện Diên Khánh, Tỉnh Khsasdfasdfjasoifdfaa",
        None,
    ),
    ("Khu Vực 4, Phường V, Thành phố Vị Thanh, Hậu Giang", "Khu Vực 4, Phường V, Thành phố Vị Thanh, Hậu Giang", 93),
    ("Phương Trù, X. Tứ Dân, H. Khóai Châu, T. Hưng Yên", "Phương Trù, X. Tứ Dân, H. Khoái Châu, T. Hưng Yên", 33),
]


def test_correct_address():
    corrector = AddressCorrector()
    for address, expected_correction, expected_code in tests:
        corrected = corrector.correct(address)
        assert str(corrected) == expected_correction
        assert corrected.province.code == expected_code
