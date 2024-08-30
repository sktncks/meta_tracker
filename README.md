# Meta Tracker
## 📝 프로젝트 소개
---
- 기능
    - Retailtrend IP 카메라에서 수집되어 처리된 vca 메타데이터를 백그라운드 영상 혹은 백그라운드 스냅샷 위에 vca 메타데이타가 가지고있는 오브젝트 정보를 결합(시각화)하여 하나의 영상으로 만드는 프로그램.
- 용도
    - Retailtrend IP 카메라가 오브젝트 정보를 올바르게 처리하여 vca 메타데이터로 변환하였는지 분석하기 쉽게 만들어주기 위한 용도.
## ⏲️ 개발 기간 
---
- 2023.05.06(목) ~ 

## 💻 개발환경 / 라이브러리
---
- **Version** : Python 3.10.12
- **IDE** : Visual Studio Code, PyCharm
- **Library (version)** :
    - click (8.1.7)
    - markdown-it-py (3.0.0)
    - mdurl (0.1.2)
    - numpy (2.0.0)
    - opencv-python (4.10.0.84)
    - Pygments (2.18.0)
    - rich (13.7.1)
    - shellingham (1.5.4)
    - typer (0.12.3)
    - typing_extensions (4.12.2)

## ⚙️ 기본 세팅 (사용 라이브러리 설치)
---
```
$ python3 ./main_setting.py
```

## 📌 기본 기능
---
help
```
$ python3 ./scr/run.py --help
```
기본 입력값
```
$ python3 ./src/run.py {metadata_path} {background_path}
```
예시
```
$ python3 ./src/run.py ./data/meta_data ./data/video_background
```



## ✒️ 필수 입력 값 설명 <br/>
---
- **metadata_path** - 메타데이터가 있는 폴더의 주소 <br/>
  *<제한 사항>*
    - 폴더안에 메타 데이터만 있어야한다.
    - 메타데이터의 이름에 영상/사진과 같은 시간정보가 들어있어야한다.
        - ex) NVD13-78-R-000DF125812F_2024-05-21T15_00_00+09_00_10m.xml

- **background_path** - 영상/사진의 주소나 영상/사진이 들어있는 폴더의 주소 <br/>
  *<제한 사항>* <br/>
    - 폴더의 주소를 입력시 폴더 안에 영상/사진만 있어야한다. <br/>
    - 영상/사진의 이름에 메타데이터들의 총 합 시간과 같은 시간정보가 들어있어야한다. <br/>
        - ex) NVD13-78-R-000DF125812F_channel1_2024-05-21T150000+0900.mp4
        - ex) NVD13-78-R-000DF125812F_channel1_2024-05-21T150000+0900.jpg

      
## ✒️ 추가 기능 입력값 정보
---
- **사용법**: -- 변경 하려고 하는 정보이름 + 변경값
    - Ex) --output-name img2video_output
- **--start-time** - 시각화 처리된 영상의 시작 시간 <br/>
    - Type: Str
    - Default: "000000"
  *<예시>*
    - 1시간짜리 메타데이터와 영상/사진에서 10분부터 작업을 원하면 001000입력
    - 00시간 00분 00초 --> 000000
- **--end-time** - 시각화 처리된 영상의 끝 시간 <br/>
    - TYPE: Str
    - Default: 입력된 메타데이터의 길이와 동일
  *<예시>* <br/>
    - 1시간짜리 메타데이터와 영상/사진에서 30분까지 작업을 원하면 003000입력 <br/>
    - 00시간 00분 00초 --> 000000 <br/>
- **--output-path** - 시각화 처리된 영상을 저장할 폴더 위치 <br/>
    - TYPE: Str
    - Default: ./
- **--output-size-rate** - 결과물의 크기변경
    - TYPE: Float
    - Default: 1
    - 값이 1보다 작으면 작아지고 1보다 커지면 원본보다 크게 변경되에 저장된다.
- **--output-name** - 시각화 처리된 영상의 이름 <br/>
    - TYPE: TEXT
    - Default: output
- **--output-extension** - 시각화 처리된 영상의 확장명 <br/>
    - TYPE: TEXT
    - Default: .avi
    
- **--box-boundary-thickness** - 오브젝트 박스 둘레의 굵기 <br/>
    - TYPE: INTEGER
    - Default: 2
- **--tail-size** - 오브젝트의 이동 동선을 보여주는 꼬리의 길이 <br/>
    - TYPE: INTEGER
    - Default: 25
- **--tail-thickness** - 오브젝트의 이동 동선을 보여주는 꼬리의 굵기 <br/>
    - TYPE: INTEGER
    - Default: 2
- **--text-scale** - 오브젝트의 아이디를 보여주는 글자의 크기 <br/>
    - TYPE: INTEGER
    - Default: 0.5
- **--text-thickness** - 오브젝트의 아이디를 보여주는 글자의 굵기 <br/>
    - TYPE: INTEGER
    - Default: 1
- **작업중 실시간으로 재생** - 영상을 시각화하는 작업 중에 시각화되는 영상을 실시간으로 재생 <br/>
    - Default: --no-visualization-on
    - 재생을 원하면: --visualization-on
- **--visualization-speed** - 실시간으로 재생되는 영상의 속도, 속도가 작을수록 재생속도 빠름
    - TYPE: INTEGER
    - Default: 50


## 💻 virtualenv
---
### 다운로드
```
$ pip install virtualenv==20.26.2
```

### 활성화
```
$ cd ./경로
```
```
$ virtualenv env --python=python3.10.12
```
```
Linux/Mac OS: source env/bin/activate
Windows: .\my_env\Scripts\activate
```

## 추후 개선사항
- Meta data를 읽어올때 stream 구조로 변경
    - 메모리 안정성 개선 가능
- AWS S3에서 직접 meta data를 가져오기