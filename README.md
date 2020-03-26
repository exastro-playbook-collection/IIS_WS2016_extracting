# IIS パラメータ生成ロール
===============================
# Trademarks
-----------
* Linuxは、Linus Torvalds氏の米国およびその他の国における登録商標または商標です。
* RedHat、RHEL、CentOSは、Red Hat, Inc.の米国およびその他の国における登録商標または商標です。
* Windows、PowerShell、IISは、Microsoft Corporation の米国およびその他の国における登録商標または商標です。
* Ansibleは、Red Hat, Inc.の米国およびその他の国における登録商標または商標です。
* pythonは、Python Software Foundationの登録商標または商標です。
* NECは、日本電気株式会社の登録商標または商標です。
* その他、本ロールのコード、ファイルに記載されている会社名および製品名は、各社の登録商標または商標です。

## Description

本ロールでは、IIS構築済み環境から設定情報を収集する機能と、収集した設定情報からIIS構築ロール(Windows版)で使用できるパラメータを生成する機能を提供します。

## Supports

本ロールは、以下環境をサポートします。

- 管理サーバー（Ansible実行サーバー）
  - OS：RHEL7.4（CentOS7.4）/RHEL8.0（CentOS8.0）
  - Ansible：Version 2.8, 2.9
  - Python：2.7 or 3.6
- 対象サーバー
  - 利用しているロール、共通部品の仕様に準拠します。

## Dependencies

本ロールでは、以下のロール、共通部品を利用しています。

- 収集機能（IIS_gathering）
  - gathering ロール
- パラメータ生成機能（IIS_extracting）
  - パラメータ生成共通部品

## Role Variables

本ロールで指定できる変数値について説明します。

### Mandatory Variables

ロール利用時に必ず指定しなければならない変数値はありません。

### Optional Variables

ロール利用時に以下の変数値を指定することができます。

- 共通

    | Name                            | Default Value | Description                        |
    | ------------------------------- | ------------- | -----------------------------------|
    |`VAR_IIS_gathering_dest`         |'{{ playbook_dir }}/_gathered_data' |収集した設定情報の格納先パス |

- IIS_extracting

    | Name                            | Default Value | Description                        |
    | ------------------------------- | ------------- | -----------------------------------|
    |`VAR_IIS_extracting_rolename`    |'['IIS_Install','IIS_Setup']'    |パラメータ生成対象 (*1) |
    |`VAR_IIS_extracting_dest`        |'{{ playbook_dir }}/_parameters' |生成したパラメータの出力先パス |

(*1) 本変数値は収集・パラメータ生成時の識別子として使用するため、通常は変更しないでください。

## Results

本ロールの出力について説明します。

### 収集した設定情報の格納先

収集した設定情報は以下のディレクトリ配下に格納します。

- <VAR_IIS_gathering_dest>/<ホスト名/IP>/IIS_WS2016_gathering/

本ロールを既定値で利用した場合、以下のように設定情報を格納します。

- Windows版 IIS の場合

    ```none
    <Playbook実行ディレクトリ>/
      +-_gathered_data/
          +-<ホスト名/IP>/
              +-IIS_WS2016_gathering/       # 収集データ
                  +-command/
                      ：
    ```

### 生成したパラメータの出力例

生成したパラメータは以下のディレクトリ・ファイル名で出力します。

- <VAR_extracting_dest>/<ホスト名/IP>/<VAR_IIS_extracting_rolename>.yml

本ロールを既定値で利用した場合、以下のようにパラメータを出力します。

- IIS の場合

    ```none
    <Playbook実行ディレクトリ>/
      +-_parameters/
          +-<ホスト名/IPアドレス>/
              +-<1|2|3|...>/
                  +-<ホスト名/IPアドレス>/
                      +-IIS_Setup.yml             # パラメータ
              +-IIS_Install.yml                       # パラメータ

    ```

## Usage

本ロールの利用例について説明します。

### 既定値で設定情報収集およびパラメータ生成を行う場合

以下の例では既定値で設定情報収集およびパラメータ生成を行います。

- `iis_pargen.yml` (IIS用Playbook)

    ```yaml
    ---
    - hosts: WindowsGroup
      gather_facts: true
      roles:
        - role: IIS_WS2016_gathering

    - hosts: WindowsGroup
      gather_facts: false
      roles:
        - role: IIS_WS2016_extracting
    ```

- 以下のように設定情報とパラメータを出力します。

    ```none
    <Playbook実行ディレクトリ>/
      +-_gathered_data/
      |   +-<ホスト名/IPアドレス>/
      |       +-IIS_WS2016_gathering/  # 収集データ
      |           +-command/
      |               ：
      +-_parameters/
          +-<ホスト名/IPアドレス>/
              +-<1|2|3|...>/
                  +-<ホスト名/IPアドレス>/
                      +-IIS_Setup.yml                 # パラメータ
              +-IIS_Setup.yml                         # パラメータ
    ```

### パラメータ再利用

以下の例では、生成したパラメータを使用して構築済IISの設定を変更します。

- `IIS_setup-playbook.yml`（IIS構築ロールを使用）

    ```yaml
    ---
    - hosts: IIS
      roles:
        - IIS_setup
    ```

- 生成したパラメータを指定してplaybookを実行

    ```sh
    ansible-playbook IIS_setup-playbook.yml -i hosts --extra-vars="@_parameters/<ホスト名/IPアドレス>/<1|2|3|...>/<ホスト名/IPアドレス>/IIS_Setup.yml"
    ```

# Copyright
---------
Copyright (c) 2019 NEC Corporation

# Author Information
------------------
NEC Corporation
