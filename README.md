# 성균관대학교 수강신청 자동화 프로그램 v0.3
#### made by Kyuwon Cho
# CAUTION!!!
본 프로그램을 사용하여 일어나는 모든 일에 대한 책임은 실행자에게 있습니다! 제작자는 당신의 강제 휴학, 정학, 징계 등에 대해 어떠한 책임도 지지 않습니다!  

## About this program
이 리포지토리는 성균관대학의 느려 터진 수강신청을 자동으로 해주는 파이썬 스크립트를 담고 있습니다. 모두 즐거운 수강신청하시길 바랍니다.

## About Security
이 프로그램은 사용자의 학번과 비밀번호를 수집하지 않습니다. 그러나 수강신청 기간동안에는 ```https```를 학교 서버에서 사용하지 않아 모든 통신은 ```http```로 갈 것입니다. 여러분의 개인정보, 안녕하십니까?

## Usage
1. 책가방에 수강신청 하고싶은 과목만 남기기
2. ```main.py```의 edit here 부분 찾아서 ID, 비밀번호 입력
3. 프로그램을 인자와 함께 실행한다
    * 아무 인자 없이 실행하면 책가방에 있는 모든 과목의 남은 TO를 구해 만일 빈 자리가 있을 경우 자동으로 수강신청을 실행한다.
    * ```-m 혹은 --main``` 옵션을 통해 본 수강신청을 실행할 수 있다. 책가방에 있는 모든 과목에 대해 책가방 정렬 순서대로 수강신청을 실행한다. 수강신청이 열리자마자 실행하는 모드이다.
    * ```--debug``` 옵션을 통해 응답을 좀 더 자세히 볼 수 있다.
    * ```--netfunnel``` 옵션을 통해 넷퍼널 키를 받을 수 있다. 특이 사항이 없으면 항상 입력하지 않는다.
4. 성공했다면 즐거운 학기를 보낸다.
5. 실패했다면 즐거운 휴학을 한다.
