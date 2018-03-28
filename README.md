
|命令（设备统一为nst0）|说明|完成后磁头位置变化
|-|-|-|
|tar -cvf /dev/nst0 文件名|写入文件|FileNumber加1，BlockNumber=0
|tar -xvf /dev/nst0 文件名|读出文件|FileNumber不变，BlockNumber变为文件末尾的block号码
|tar -tvf /dev/nst0|列出文件列表|FileNumber不变，BlockNumber变为文件末尾的block号码
|mt -f /dev/nst0 status|查看磁头位置|不变
|mt -f /dev/nst0 rewind|回卷磁头|FileNumber=0，BlockNumber=0
|mt -f /dev/nst0 eod|移到数据末尾|FileNumber为最大加1，BlockNumber=-1
|mt -f /dev/nst0 fsf 数字|前进磁头，定位在后一个文件的第一块上|FileNumber为当前File号码+数字，BlockNumber=0
|mt -f /dev/nst0 fsfm 数字|前进磁头，定位在前一个文件的最后块上|FileNumber为当前File号码+数字-1，BlockNumber=-1
|mt -f /dev/nst0 bsf 数字|倒退磁头，定位在前一个文件的最后块上|FileNumber为当前File号码-数字，BlockNumber=-1
|mt -f /dev/nst0 bsfm 数字|倒退磁头，定位在后一个文件的第一块上|FileNumber为当前File号码-数字+1，BlockNumber=0