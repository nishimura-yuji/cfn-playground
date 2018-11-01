## 作成したテンプレートをまとめるレポジトリ

## fabric

Fabric は Python のモジュール(例えば fabfile.py)やパッケージ(例えば **init**.py を含んでいる fabfile/ ディレクトリ)を読み込むことができます。デフォルトでは、(Python のインポート機構にしたがって) fabfile と名付けられた fabfile/ もしくは fabfile.py を探します。

fabfile の探索アルゴリズムは、起動しているユーザーのカレントワーキングディレクトリやその親ディレクトリを探します。したがって、”プロジェクト” ユース周り指向で、例えばコードツリーのルートに fabfile.py を保持しておきます。こうした fabfile は、ユーザーが fab を呼び出すツリー内であればどこであれ見つけられます。

そのため、fablic/配下にファイルをおけば

```
$ fab -l
```

で実行関数を表示してくれる

## テンプレート作成方針

- テンプレートのパラメータには必ず環境設定を入れる

```
Parameters:
  StageName:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - stage
      - prod
    Description: デプロイ対象のステージ名
```

- 環境依存、テンプレート間のやりとりはParamater storeを使う

別テンプレートにリソース名など値を渡す

```
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.250.252.0/24
  SSMVpcId: # 渡す値をParameter Storeに保存する
    Type: AWS::SSM::Parameter
    Properties:
      Name: /cf-values/VpcId
      Type: String
      Value: !Ref 'VPC'
```



別テンプレートからリソース名など値を受け取る

```
AWSTemplateFormatVersion: '2010-09-09'
Parameters:
  VpcId: # 受け取る値を定義する
    Type: AWS::SSM::Parameter::Value<AWS::EC2::VPC::Id>
    Default: /cf-values/VpcId # Parameter StoreのNameを指定
Resources:
  Subnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VpcId
      CidrBlock: 10.250.252.0/28
```

または
```{{resolve:ssm:S3AccessControl:2}}```で受け取ることができる

```
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  Subnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: '{{resolve:ssm:S3AccessControl:2}}'
      CidrBlock: 10.250.252.0/28
```