Proj_4 EMD
=======================

### Installation 安裝

 1. 環境建議使用 `Ubuntu 1404` (`Linux` 的一個發行版)
 2. 安裝 `Python 3` 並且把 `pip` (`Python` 套件管理工具) 安裝好
    1. 範例指令：`sudo apt-get update && sudo apt-get -y install python3 python3-pip`
 3. 把本作業需要的套件安裝好
    1. 範例指令：`sudo pip-3.2 install -r <本作業目錄>/requirements.txt` (`pip-3.2` 的部分會因版本而有所不同 )

### Usage 使用方式 (從 Python Script 執行)

```
Usage:
    python[3] emd.py [-D] <n> <image_path>

Option:
    -D : debug mode (enable verbose)
```

啟用 `-D` 時，會把過程訊息顯示出

### 結果

執行

```
python emd.py 4 test/lena.bmp
```

會得到

```
Starting ...
== Result =========================
EMbed number:  65536
MSE: 0.22243118286132812
PSNR: 54.65884689489865
```
