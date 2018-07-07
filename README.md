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
