Proj_2 Opap Steganogrpah
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
    python[3] conceal.py [-ORmv<k>] <input_img> [result_img] [secret_msg]

    [-LRv] flags:
    -O : Skip OPAP
    -R : Reverse the operation, get the secret message from the <input_img>
    -m : Use a string as the secret message, the [secret_msg] is required when concealing
   <k> : the k value from `1` - `8`
    -v : show debug message
```

不指定 `k` 值時，將使用 `3` 作為預設值  

請注意本作業是以 `Python 3` 撰寫而成，所以必須要保證呼叫之直譯器版本為 `Python 3`  

啟用 `-O` 時，表示純粹使用 `LSB` 方法  

#### 從包好的 `exe` 檔案執行 (For windows)

同樣需要使用 `cmd` 來呼叫，呼叫之執行檔為 `<本專案目錄>\dist\conceal.exe` ，用來代替原本指令的 `python[3] conceal.py` 部分即可  

以  OPAP Steganogrpah (Random) 為例：  

```
.\dist\conceal.exe <input_img> <result_img>
```

> 此 EXE 執行檔案是由 [py2exe](https://pypi.python.org/pypi/py2exe/) 產生

#### Usage 1: Conceal the Random Message using OPAP Steganogrpah

Simply  

```
python[3] conceal.py <input_img> <result_img>
```

例如：  

```
python[3] conceal.py .\test\goldhill.bmp .\test\goldhill_k3.bmp
```

會把 `test/goldhill.png` 作為來源，產生 `test/goldhill_k3.png` ， 並且顯示出 MSE 以及 PSNR (此時使用之 `k` 值為 `3`)：  

```
MSE = 5.4963531494140625 PSNR = 40.7300573181013
```

若需要指定 `k` 值，加上 `-<k>` 即可，例如下方指令會使用 `5` 作為 `k` 值：  

```
python[3] conceal.py -5 .\test\goldhill.bmp .\test\goldhill_k5.bmp
```

並且顯示出 MSE 以及 PSNR ：  

```
MSE = 85.31536483764648 PSNR = 28.820531085597576
```

#### Usage 2: Check the Random Message when concealing

啟用 `v` flag，會把藏入的數值印出，由於印出的資料量龐大，請用 CMD / 終端機的導向至檔案功能 (指令後方加上 `> 檔案名稱`)：   

```
python[3] conceal.py -v <input_img> <result_img> > <stdout_to_this_file>
```

例如：  

```
python[3] conceal.py -v .\test\goldhill.bmp .\test\goldhill_k3.bmp > .\test\goldhill_k3_forward.txt
```

結束後 `.\test\goldhill_k3_forward.txt` 的檔案內容可以看到藏入的數字：  

```
=========================================
1 0 2 1 6 2 6 5 0 1 4 0 7 6 1 6 4 0 3 2 1 6 1 7 6 1 2 1 2 5 5 4 1 6 7 0 ...
```

#### Usage 3: Reveal the Random Message

啟用 `R` flag，使用 `Usage 1` 產生的 `<result_img>` 作為 `<input_img>` ，且不需要給予 `<result_img>` ，由於印出的資料量龐大，請用 cmd / 終端機的導向至檔案功能 (指令後方加上 `> 檔案名稱`)：  

```
python[3] conceal.py -R <input_img> > <stdout_to_this_file>
```

例如：  

```
python[3] conceal.py -R .\test\goldhill_k3.bmp > .\test\goldhill_k3_backward.txt
```

結束後 `.\test\goldhill_k3_backward.txt` 的檔案內容可以看到藏入的數字：  

```
Reversing the message out ...
1 0 2 1 6 2 6 5 0 1 4 0 7 6 1 6 4 0 3 2 1 6 1 7 6 1 2 1 2 5 5 4 1 6 7 0 ...
```

理論上應該和 `Usage 2` 中所示的藏入數字相同  

#### Usage 4: Conceal A Specified String using OPAP Steganogrpah

啟用 `m` flag，並給予 `[secret_msg]` ，其餘和 `Usage 1` 相同：  

```
python[3] conceal.py -m <input_img> <result_img> <secret_msg>
```

若 `secret_msg` 中有空白鍵 ` ` ，請把 `secret_msg` 用 `"` 包起來如下所示：  

```
python[3] conceal.py -m <input_img> <result_img> "<secret_msg>"
```

例如：  

```
python[3] conceal.py -m .\test\goldhill.bmp .\test\goldhill_k3_m.bmp "老師你好，這是 4101056017 邱冠喻 Assignment2 的測試資料 This is utf-8 encoded"
```

產生之 `.\test\goldhill_k3_m.bmp` 內藏有 `老師你好，這是 4101056017 邱冠喻 Assignment2 的測試資料 This is utf-8 encoded` 這個訊息，下方 `Usage 5` 將介紹解開的方法  

#### Usage 5: Reveal A Specified String

啟用 `R` 與 `m` flag，使用 `Usage 4` 產生的 `<result_img>` 作為 `<input_img>` ，且不需要給予 `<result_img>` ：  

```
python[3] conceal.py -Rm <input_img>
```

例如：  

```
python[3] conceal.py -Rm .\test\goldhill_k3_m.bmp
```

理論上可以把原本  `Usage 4` 藏入的字串拿出來：  

```
Message revealed:
=========================================
 老師你好，這是 4101056017 邱冠喻 Assignment2 的測試資料 This is utf-8 encoded
=========================================
```
