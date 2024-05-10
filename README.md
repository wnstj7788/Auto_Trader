# smtm
[![build status](https://github.com/msaltnet/smtm/actions/workflows/python-test.yml/badge.svg)](https://github.com/msaltnet/smtm/actions/workflows/python-test.yml)
[![license](https://img.shields.io/github/license/msaltnet/smtm.svg?style=flat-square)](https://github.com/msaltnet/smtm/blob/master/LICENSE)
![language](https://img.shields.io/github/languages/top/msaltnet/smtm.svg?style=flat-square&colorB=green)
[![codecov](https://codecov.io/gh/msaltnet/smtm/branch/master/graph/badge.svg?token=USXTX7MG70)](https://codecov.io/gh/msaltnet/smtm)

> It's a game to get money. 

파이썬 알고리즘기반 암호화폐 자동매매 프로그램. https://smtm.msalt.net

[English](https://github.com/msaltnet/smtm/blob/master/README-en_us.md) 👈

[![icon_wide_gold](https://user-images.githubusercontent.com/9311990/161744914-05e3d116-0e9b-447f-a015-136e0b9ec22b.png)](https://smtm.msalt.net/)

"데이터 수집🔍 ➡️ 알고리즘 분석🖥️ ➡️ 실시간 거래💸" 프로세스를 정해진 간격으로 반복 수행

1. Data Provider 모듈이 데이터 취합  
2. Strategy 모듈을 통한 알고리즘 매매 판단  
3. Trader 모듈을 통한 거래 처리  
 --- 반복 ---
4. Analyzer 모듈을 통한 분석

❗ 초 단위의 짧은 시간에 많은 거래를 처리해야하는 고성능 트레이딩 머신으로는 적합하지 않으며 충분한 검토가 필요합니다.

![smtm-procedure](https://github.com/msaltnet/smtm/assets/9311990/1455246e-90c2-4093-8345-33276ebae50b)

## 주요기능
- 멀티프로세스 대량시뮬레이션
- Jupyter Notebook을 활용 원격컨트롤
- 텔레그램 챗봇 자동거래 프로그램

텔레그램 메신저를 사용해서 자동매매 프로그램 컨트롤

![smtm_bot](https://user-images.githubusercontent.com/9311990/150667094-95139bfb-03e0-41d5-bad9-6be05ec6c9df.png)

![smtm-telegram-mode](https://github.com/msaltnet/smtm/assets/9311990/22ba2ebd-13e6-4eee-a829-94209c5618a9)

## Architecture
확장성과 유지보수성을 갖춘 Layered Architecture


![smtm component](./doc/smtm_component.png)

