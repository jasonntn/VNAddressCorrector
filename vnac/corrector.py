import copy
import re
from typing import List, Tuple, Union

import rapidjson
from loguru import logger
from rapidfuzz import fuzz, process
from rapidfuzz.distance import Indel
from vietnam_provinces import NESTED_DIVISIONS_JSON_PATH

from vnac.schemas import Address


class AddressCorrector:
    _prefix_pattern = re.compile(
        r"^(Tỉnh|Thành phố|Quận|Huyện|Thị xã|Phường|Xã|Thị trấn|TP[.]|TP\s|T[.]|T\s|H[.]|H\s|TX[.]|TX\s|P[.]|P\s|X[.]|X\s|)\s*(.*)", re.I
    )
    similarity_threshold = 0.75

    def __init__(self):
        with NESTED_DIVISIONS_JSON_PATH.open(encoding="utf-8") as f:
            self.db = rapidjson.load(f)

        self.provinces = {}
        self.districts = {}
        self.wards = {}
        for province in self.db:
            province_name = self._prefix_pattern.findall(province["name"])[0][1]
            self.provinces.update({province_name: province["code"]})
            for district in province["districts"]:
                district_name = self._prefix_pattern.findall(district["name"])[0][1]
                self.districts.update({district_name: district["code"]})
                for ward in district["wards"]:
                    ward_name = self._prefix_pattern.findall(ward["name"])[0][1]
                    self.wards.update({ward_name: ward["code"]})
        self.provinces["HCM"] = 79

    @classmethod
    def find_best_match(cls, query: str, choices: List[str], threshold: float = 0.8) -> Tuple[str, float]:
        match = None
        score = 0
        res = process.extractOne(
            query,
            choices,
            scorer=Indel.normalized_similarity,
            score_cutoff=threshold,
            processor=lambda s: s.title(),
        )
        if res:
            match, score = res[:2]
            logger.debug(f"Best global match: {query} ~ {match} = {score:.4f}")
        return match, score

    @classmethod
    def correct_best_match(cls, src: str, dst: str, threshold: float = 0.8) -> Tuple[str, float]:
        corrected = None
        score = 0
        src = " " + src + " "
        dst = " " + dst + " "
        res = fuzz.partial_ratio_alignment(src, dst, score_cutoff=threshold * 100)
        if res:
            src_match = src[res.src_start : res.src_end].strip()
            dst_match = dst[res.dest_start : res.dest_end].strip()
            score = res.score
            corrected = src.replace(src_match, dst_match).strip()
            logger.debug(f"Best local  match: {src_match} ~ {dst_match} = {score/100:.4f}")
        return corrected, score

    def correct_region(self, region: str, regions: List[str]) -> Tuple[str, str]:
        prefix, name = self._prefix_pattern.findall(region)[0]
        match = None
        corrected = None

        match, match_score = self.find_best_match(name, regions, threshold=self.similarity_threshold)
        # Skip if no match region found or region already correct
        if match_score != 0.0 and match_score != 1.0:
            corrected, corrected_score = self.correct_best_match(name, match, threshold=self.similarity_threshold)
            if corrected:
                if corrected_score < match_score:
                    corrected = match
                else:
                    corrected = (prefix + " " + corrected).strip()
                logger.debug("Corrected: {} -> {}", region, corrected)

        return match, corrected

    def correct(self, address: Union[Address, str]) -> Address:
        if isinstance(address, str):
            address = Address.from_str(address)
        corrected_address = copy.deepcopy(address)

        if address.province:
            match_province, corrected_province = self.correct_region(address.province.name, self.provinces.keys())
            if corrected_province:
                corrected_address.province.name = corrected_province
            if match_province:
                corrected_address.province.code = self.provinces[match_province]

        if address.district:
            _, corrected_district = self.correct_region(address.district.name, self.districts.keys())
            if corrected_district:
                corrected_address.district.name = corrected_district

        if address.ward:
            _, corrected_ward = self.correct_region(address.ward.name, self.wards.keys())
            if corrected_ward:
                corrected_address.ward.name = corrected_ward
        logger.info("Before: {}", address)
        logger.info("After : {}", corrected_address)
        return corrected_address


if __name__ == "__main__":
    import time

    tests = [
        "Nhi Bình, Châu Thanh, Tiền Giang",
        "Số 36A Đường 29, Ấp Tân Tiến, Tân Thìng Hội, Củ Chí, HCM",
        "TP. Hô Ch Minh",
        "Biên Hòa, Đng Nai",
        "HẢI PHÒNG",
        "Nốt Bình, Châu Thơng, Biên Giang",
        "Số 09 Hoàng Văn Thụ, Phường Tân An, TP.Buôn Ma Thuột, Tỉnh ĐắkLắk",
        "Thôn Cây Sung, Xã DiênTân, Huyện Diên Khánh, Tỉnh Khánh Hòa",
        "Thôn Cây Sung, Xã DiênTân, Huyện Diên Khánh, Tỉnh Khsasdfasdfjasoifdfaa",
        "Khu Vực 4, Phường V, Thành phố Vị Thanh, Hậu Giang",
        "Phương Trù, X. Tứ Dân, H. Khóai Châu, T. Hưng Yên",
    ]
    corrector = AddressCorrector()
    times = []
    for test in tests:
        start = time.time()
        address = Address.from_str(test)
        result = corrector.correct(address)
        times.append(time.time() - start)
        logger.debug(times[-1])
    logger.debug(sum(times) / len(times))
