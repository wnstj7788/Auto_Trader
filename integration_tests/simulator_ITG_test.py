import unittest
from smtm import Simulator, Config
from unittest.mock import *


class SimulatorIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.interval = Config.candle_interval
        Config.candle_interval = 60

    def tearDown(self):
        Config.candle_interval = self.interval

    @patch("builtins.print") # print 함수를 mock 으로 대체
    def test_ITG_run_single_simulation(self, mock_print): # 한 번의 실행이 설정부터 처리되는 run_single 메서드 검증 
        interval = 0.01
        from_dash_to = "200430.055000-200430.073000"
        simulator = Simulator(  # 예산과 시뮬레이션 턴의 간격, 사용될 전략, 시뮬레시연 기간을 simulator 생성자를 통해 생성함 
            budget=1000000,
            interval=interval,
            strategy="BNH",
            from_dash_to=from_dash_to,
            currency="BTC",
        )

        simulator.run_single()
        self.assertEqual(mock_print.call_args[0][0], "Good Bye~")



    # 사용자의 입력을 기반으로 Simlutor가 동작하는 동작 검증 
    @patch("builtins.input") 
    @patch("builtins.print") 
    def test_ITG_run_simulation(self, mock_print, mock_input):
        simulator = Simulator()
        mock_input.side_effect = [ # Mock 객체를 통해 사용자가 직접 입력한 것 처럼 만들기 
            "i",  # 초기화
            "200430.055000",  # 시뮬레이션 기간 시작점
            "200430.073000",  # 시뮬레이션 기간 종료점
            "0.1",  # interval
            "1000000",  # budget
            "BNH",  # strategy
            "ETH",  # currency
            "1",  # 상태 출력
            "r",  # 시뮬레이션 시작
            "1",  # 상태 출력
            "s",  # 시뮬레이션 종료
            "3",  # 거래 내역 출력
            "1",  # 상태 출력
            "2",  # 수익률 출력
            "t",  # 시뮬레이터 종료
        ]
        simulator.main()

        expected_score = [
            "ready",
            "current score ==========",
            "Good Bye~",
        ]

        self.assertEqual(mock_print.call_args_list[-1][0][0], expected_score[2])
        self.assertEqual(mock_print.call_args_list[-6][0][0], expected_score[1])
        self.assertEqual(mock_print.call_args_list[-7][0][0], expected_score[0])

class SimulatorWithDualIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.dp_type = Config.simulation_data_provider_type
        self.interval = Config.candle_interval
        Config.candle_interval = 60
        Config.simulation_data_provider_type = "dual"

    def tearDown(self):
        Config.candle_interval = self.interval
        Config.simulation_data_provider_type = self.dp_type

    @patch("builtins.print")
    def test_ITG_run_single_simulation(self, mock_print):
        interval = 0.01
        from_dash_to = "200430.055000-200430.073000"
        simulator = Simulator(
            budget=1000000,
            interval=interval,
            strategy="BNH",
            from_dash_to=from_dash_to,
            currency="BTC",
        )

        simulator.run_single()
        self.assertEqual(mock_print.call_args[0][0], "Good Bye~")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_ITG_run_simulation(self, mock_print, mock_input):
        simulator = Simulator()
        mock_input.side_effect = [
            "i",  # 초기화
            "200430.055000",  # 시뮬레이션 기간 시작점
            "200430.073000",  # 시뮬레이션 기간 종료점
            "0.1",  # interval
            "1000000",  # budget
            "BNH",  # strategy
            "ETH",  # currency
            "1",  # 상태 출력
            "r",  # 시뮬레이션 시작
            "1",  # 상태 출력
            "s",  # 시뮬레이션 종료
            "3",  # 거래 내역 출력
            "1",  # 상태 출력
            "2",  # 수익률 출력
            "t",  # 시뮬레이터 종료
        ]
        simulator.main()

        expected_score = [
            "ready",
            "current score ==========",
            "Good Bye~",
        ]

        self.assertEqual(mock_print.call_args_list[-1][0][0], expected_score[2])
        self.assertEqual(mock_print.call_args_list[-6][0][0], expected_score[1])
        self.assertEqual(mock_print.call_args_list[-7][0][0], expected_score[0])
