Proj_1 Color Transfer
=======================

### Installation 安裝

 1. 環境建議使用 `Ubuntu 1404` (`Linux` 的一個發行版)
 2. 安裝 `Python 3` 並且把 `pip` (`Python` 套件管理工具) 安裝好
    1. 範例指令：`sudo apt-get update && sudo apt-get -y install python3 python3-pip`
 3. 把本作業需要的套件安裝好
    1. 範例指令：`sudo pip-3.2 install -r <本作業目錄>/requirements.txt` (`pip-3.2` 的部分會因版本而有所不同 )

### Usage 使用方式

```
Usage:
    python[3] transColor.py [-ROMbav] <source_img> <target_img> <destination_img> [source_avg_r source_avg_g source_avg_b source_dev_r source_dev_g source_dev_b]

    [-ROMbav] flags:
    -R : reverse the operation, source_img will be treated as the converted img, flag M will be enable, flag b,a will be disabled and source_avg and source_dev is required
    -O : disable log at convertion
    -M : disable lms at convertion (Use pure RGB to convert) (Also disable log)
    -b : use boundary to convert instead of statistics method
    -a : adjust the result to source boundary
    -v : show debug message
```

請注意本作業是以 `Python 3` 撰寫而成，所以必須要保證呼叫之直譯器版本為 `Python 3`

#### Command for Program 1: Reinhard Color Transfer (Using LMS)

Simply

```
python[3] transColor.py <source_img> <target_img> <destination_img>
```

for example:

```
python3 transColor.py test/01.png test/02.png test/01-02.png
```

會把 `test/01.png` 作為來源， `test/02.png` 作為目標， 產生出 `test/01-02.png`

#### Command for Program 2: RGB Color Transfer

啟用 `M` flag，例如

```
python3 transColor.py -M test/01.png test/02.png test/01-02_RGB.png
```

會把 `test/01.png` 作為來源， `test/02.png` 作為目標， 產生出 `test/01-02_RGB.png`

#### Command for Program 3: MSE and PSNR

每次執行轉換時都對把 `<source_img>` 以及 `<destination_img>` 的 MSE 以及 PSNR 顯示出來，例如

```
MSE between source and destination is 202.200272
PSNR between source and destination is 25.072986
```

#### Command for Program 4: Reverse RGB ‐ Color Transfer

啟用 `R` flag，使用轉換過的圖放置在 `<source_img>` 的欄位，並且輸入原始圖的 三色平均值以及三色標準差，例如

```
python3 transColor.py -R test/416-856.bmp test/856.bmp test/416-856-back.bmp 0.45171131807220521 0.49474325741038383 0.5059502545525576 0.18720403573878344 0.1863502133550516 0.2658009087882103
```

平均值以及標準差可以是 1 ~ 255 或者 0 ~ 1 皆可，程式會自動判斷，另外平均值可以在正向轉換時顯示出來：

```
src_avg [0.45171131807220521, 0.49474325741038383, 0.5059502545525576]
src_dev [0.18720403573878344, 0.1863502133550516, 0.2658009087882103]
```
