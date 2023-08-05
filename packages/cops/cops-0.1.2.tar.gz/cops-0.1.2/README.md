

# Feature

* Support multiple accounts



# 設計

使用者

- Infra Team
- Dev and QA Team


---

## 環境需求

* python 2.7.x
* pip
  * boto3 (AWS SDK): `pip install boto3`
  * PyYaml: `pip install PyYaml`

## AWS IAM 權限

增加 IAM Policy 給使用者：`./docs/iam-policy.json`

0. aws account, ak/sk
1. setup.py



## 設定環境變數

* AWS_DEFAULT_PROFILE: 指定 AWS Profile. **(required)**
* AWS_DEFAULT_REGION: 指定 AWS Region **(required)**
* COPS_HOME: 指定 `cloudops` 的路徑 **(required)**
* COPS_USERDATA: 指定 AWS 資源設定的路徑 **(optional)**
  * 此路徑的資料與設定檔可以 commit 到 source control.
  * 如果沒有設定此變數就是目前位置 `.`

## Linux / OS X

在 `~/.bashrc` 加入以下環境變數：

```bash
export AWS_DEFAULT_REGION=ap-northeast-1
export AWS_DEFAULT_PROFILE=<profile_name>

export COPS_HOME=</path/to/put/cloudops>
export COPS_USERDATA=</userdata/example/etc>

export PATH=$COPS_HOME:$PATH
```

<!--
### Windows 在系統變數設定

在 `系統環境變數` 設定環境變數
-->


### COPS_USERDATA 資料結構

此路徑的結構如下：

```
.
├── IAM
├── <region>
├── ap-northeast-1
│   ├── ec2
│   └── security_groups
└── ap-southeast-1
    ├── ec2
    └── security_groups

```


---
# 準備工作



* VPCs
* Security Groups
* Template Configs



---
# 使用方式

* 確認安裝正確：再任意路徑執行 `cloudops.py` 會出現 help 資訊
* 切換到 `COPS_USERDATA`: `cd $COPS_USERDATA`
* 用 Editor 修改 `${AWS_DEFAULT_PROFILE}/${AWS_DEFAULT_REGION}/ec2` 的 EC2 設定檔
* 執行建立 EC2: `cloudops.py --ec2 <EC2_CONFIG>.yml`: <EC2_CONFIG> 會自動找 `${COPS_USERDATA}` 底下的檔案


## 使用情境

Infra / Ops Team

define server type:

- web/networking.yaml
- web/networking.yaml
- web/networking.yaml
- web/networking.yaml



cloudops.py --ec2 <EC2_CONFIG>.yml


更多說明請參閱 `FEATURE.md`


## 確認 EC2 Instance 是否正常

* 確認 Tags 是否如預期
* 確認 ENIs 是否如設定
* 確認 EBS 是否如指定大小與 Type
* 確認 Userdata 執行結果：
  * AWS Linux & Ubuntu: `/var/log/cloud-init-output.log`
  * Windows: `C:\Program Files\Amazon\Ec2ConfigService\Logs\Ec2ConfigLog.txt`


## 參考

* [Configuring the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
* [cloud-init](https://cloudinit.readthedocs.io/en/latest/index.html)
