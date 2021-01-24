"""거래 요청, 결과 정보를 저장하고 투자 결과를 분석

이 모듈은 거래 요청, 결과 정보를 저장하고 투자 결과를 분석하는 클래스인 Analayzer를 포함하고 있다.
"""
import time
import copy
from datetime import datetime, timedelta
from .log_manager import LogManager


class Analyzer:
    """거래 요청, 결과 정보를 저장하고 투자 결과를 분석하는 클래스

    Attributes:
        request: 거래 요청 정보 목록
        result: 거래 결과 정보 목록
        asset_record_list: 특정 시점에 기록된 자산 정보 목록
        score_record_list: 특정 시점에 기록된 수익률 정보 목록
        update_info_func: 자산 정보 업데이트를 요청하기 위한 콜백 함수

    """

    ISO_DATEFORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self):
        self.request = []
        self.result = []
        self.infos = []
        self.asset_record_list = []
        self.score_record_list = []
        self.update_info_func = None
        self.logger = LogManager.get_logger(__name__)
        self.is_simulation = False

    def put_trading_info(self, info):
        self.infos.append(info)

    def put_request(self, request):
        """거래 요청 정보를 저장한다"""
        try:
            if request["price"] <= 0 or request["amount"] <= 0:
                return
        except KeyError:
            self.logger.warning("Invalid request")
            return

        self.request.append(copy.deepcopy(request))

    def put_result(self, result):
        """거래 결과 정보를 저장한다"""
        if self.update_info_func is None:
            self.logger.warning("update_info_func is NOT set")
            return
        try:
            if result["price"] <= 0 or result["amount"] <= 0:
                return
        except KeyError:
            self.logger.warning("Invalid result")
            return

        self.result.append(copy.deepcopy(result))
        self.update_info_func("asset", self.put_asset_info)

    def initialize(self, update_info_func, is_simulation=False):
        """콜백 함수를 입력받아 초기화한다

        Args:
            update_info_func: 거래 데이터를 요청하는 콜백 함수로 func(arg1, arg2) arg1은 정보 타입, arg2는 콜백 함수

        """
        self.update_info_func = update_info_func
        self.is_simulation = is_simulation

    def put_asset_info(self, asset_info):
        """자산 정보를 저장한다"""
        self.asset_record_list.append(copy.deepcopy(asset_info))
        self.make_score_record(asset_info)

    def make_start_point(self):
        """시작시점 거래정보를 기록한다"""
        self.request = []
        self.result = []
        self.asset_record_list = []
        self.update_info_func("asset", self.put_asset_info)

    def make_score_record(self, new_info):
        """수익률 기록을 생성한다

        Args:
            balance: 계좌 현금 잔고
            cumulative_return: 기준 시점부터 누적 수익률
            price_change_ratio: 기준 시점부터 보유 종목별 가격 변동률 딕셔너리
            asset: 자산 정보 튜플 리스트 (종목, 평균 가격, 현재 가격, 수량, 수익률(소숫점3자리))
            date_time: 데이터 생성 시간, 시뮬레이션 모드에서는 데이터 시간 +3초
        """

        try:
            now = datetime.now().strftime(self.ISO_DATEFORMAT)

            if self.is_simulation:
                last_dt = datetime.strptime(self.infos[-1]["date_time"], self.ISO_DATEFORMAT)
                now = last_dt + timedelta(seconds=3)
                now = now.isoformat()

            start_total = self.__get_start_property_value()
            start_quote = self.asset_record_list[0]["quote"]
            current_total = new_info["balance"]
            current_quote = new_info["quote"]
            cumulative_return = 0
            new_asset_list = []
            price_change_ratio = {}
            self.logger.info(f"quote {current_quote}")

            for name, item in new_info["asset"].items():
                item_yield = 0
                price = current_quote[name]
                current_total += item[1] * price
                item_price_diff = price - item[0]
                if item_price_diff != 0:
                    item_yield = (price - item[0]) / item[0] * 100
                    item_yield = round(item_yield, 3)

                self.logger.info(
                    f"yield record {name}, {item[0]}, {price}, {item[1]}, {item_yield}"
                )
                new_asset_list.append((name, item[0], price, item[1], item_yield))
                start_price = start_quote[name]
                price_change_ratio[name] = 0
                price_diff = price - start_price
                if price_diff != 0:
                    price_change_ratio[name] = price_diff / start_price * 100
                    price_change_ratio[name] = round(price_change_ratio[name], 3)
                self.logger.info(
                    f"price change ratio {start_price} -> {price}, {price_change_ratio[name]}%"
                )

            total_diff = current_total - start_total
            if total_diff != 0:
                cumulative_return = (current_total - start_total) / start_total * 100
                cumulative_return = round(cumulative_return, 3)
            self.logger.info(
                f"cumulative_return {start_total} -> {current_total}, {cumulative_return}%"
            )

            self.score_record_list.append(
                {
                    "balance": new_info["balance"],
                    "cumulative_return": cumulative_return,
                    "price_change_ratio": price_change_ratio,
                    "asset": new_asset_list,
                    "date_time": now,
                }
            )
        except (IndexError, AttributeError):
            self.logger.error("making score record fail")

    def create_report(self, filename="report.txt"):
        """수익률 보고서를 생성한다

        Args:
            filename: 생성할 리포트 파일명
        Returns:
            {
                "summary": (
                    cumulative_return: 기준 시점부터 누적 수익률
                    price_change_ratio: 기준 시점부터 보유 종목별 가격 변동률 딕셔너리
                    asset: 자산 정보 튜플 리스트 (종목, 평균 가격, 현재 가격, 수량, 수익률(소숫점3자리))
                    date_time: 데이터 생성 시간, 시뮬레이션 모드에서는 데이터 시간 +3초
                ),
                "trading_table" : [
                    {
                        "date_time": 생성 시간, 정렬 기준 값
                        거래 정보, 매매 요청 및 결과 정보, 수익률 정보 딕셔너리
                    }
                ]
            }
        """
        self.update_info_func("asset", self.put_asset_info)
        try:
            list_sum = self.request + self.infos + self.score_record_list + self.result
            trading_table = sorted(
                list_sum, key=lambda data: datetime.strptime(data["date_time"], self.ISO_DATEFORMAT)
            )
            start_value = self.__get_start_property_value()
            last_value = self.__get_last_property_value()
            last_return = self.score_record_list[-1]["cumulative_return"]
            change_ratio = self.score_record_list[-1]["price_change_ratio"]
            summary = (start_value, last_value, last_return, change_ratio)
            self.logger.info("### Analyzer Report ===============================")
            self.logger.info(f"Property                 {start_value:10} -> {last_value:10}")
            self.logger.info(
                f"Gap                                    {last_value - start_value:10}"
            )
            self.logger.info(f"Cumulative return                    {last_return:10} %")
            self.logger.info(f"Price_change_ratio {change_ratio}")
            self.__create_report_file(filename, summary, trading_table)
            return {"summary": summary, "trading_table": trading_table}
        except (IndexError, AttributeError):
            self.logger.error("create report FAIL")

    def __create_report_file(self, filepath, summary, trading_table):
        """
        ### TRADING TABLE =================================
        {date_time}, {opening_price}, {high_price}, {low_price}, {closing_price}, {acc_price}, {acc_volume}
        2020-02-23T00:00:00, 5000, 15000, 4500, 5500, 1500000000, 1500

        {date_time}, [->] {id}, {type}, {price}, {amount}
        2020-02-23T00:00:01, 1607862457.560075, sell, 1234567890, 1234567890

        {date_time}, [<-] {request_id}, {type}, {price}, {amount}, {msg}, {balance}
        2020-02-23T00:00:01, 1607862457.560075, sell, 1234567890, 1234567890, success, 1234567890

        {date_time}, [#] {balance}, {cumulative_return}, {price_change_ratio}, {asset}
        2020-02-23T00:00:01, 1234567890, 1234567890, 1234567890, 1234567890

        ### SUMMARY =======================================
        Property                 1234567890 -> 1234567890
        Gap                                    1234567890
        Cumulative return                    1234567890 %
        Price_change_ratio {'mango': -50.0, 'apple': 50.0}
        """

        with open(filepath, "w") as f:
            if len(trading_table) > 0:
                f.write("### TRADING TABLE =================================\n")

            for item in trading_table:
                if "opening_price" in item:
                    f.write(
                        f"{item['date_time']}, {item['opening_price']}, {item['high_price']}, {item['low_price']}, {item['closing_price']}, {item['acc_price']}, {item['acc_volume']}\n"
                    )
                if "id" in item:
                    f.write(
                        f"{item['date_time']}, [->] {item['id']}, {item['type']}, {item['price']}, {item['amount']}\n"
                    )
                if "request_id" in item:
                    f.write(
                        f"{item['date_time']}, [<-] {item['request_id']}, {item['type']}, {item['price']}, {item['amount']}, {item['msg']}, {item['balance']}\n"
                    )
                if "cumulative_return" in item:
                    f.write(
                        f"{item['date_time']}, [#] {item['balance']}, {item['cumulative_return']}, {item['price_change_ratio']}, {item['asset']}\n"
                    )

            f.write("### SUMMARY =======================================\n")
            f.write(f"Property                 {summary[0]:10} -> {summary[1]:10}\n")
            f.write(f"Gap                                    {summary[1] - summary[0]:10}\n")
            f.write(f"Cumulative return                    {summary[2]:10} %\n")
            f.write(f"Price_change_ratio {summary[3]}\n")

    def __get_start_property_value(self):
        return round(self.__get_property_total_value(0))

    def __get_last_property_value(self):
        return round(self.__get_property_total_value(-1))

    def __get_property_total_value(self, index):
        total = self.asset_record_list[index]["balance"]
        quote = self.asset_record_list[index]["quote"]
        for name, item in self.asset_record_list[index]["asset"].items():
            total += item[1] * quote[name]
        return total
