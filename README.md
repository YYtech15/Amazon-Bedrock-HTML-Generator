# Amazon Bedrock HTML Generator

このプロジェクトは、Amazon Bedrock APIを使用して生成AIモデルにプロンプトを送信し、その結果をHTMLとして表示するFlaskウェブアプリケーションです。

## 機能

- ユーザーがテキストプロンプトを入力できる対話型ウェブインターフェース
- Amazon Bedrock APIを使用したAI生成HTMLコンテンツの取得
- 生成されたHTMLコンテンツのリアルタイムプレビュー
- 複数回の対話を通じたコンテンツの改善機能

## 必要条件

- Python 3.7以上
- AWSアカウントとAmazon Bedrockへのアクセス権限
- 必要なPythonパッケージ（requirements.txtに記載）

## セットアップ

1. リポジトリをクローンまたはダウンロードします。

2. 必要なパッケージをインストールします：
   ```
   pip install -r requirements.txt
   ```

3. `.env`ファイルを作成し、以下のAWS認証情報を記入します：
   ```
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_DEFAULT_REGION=your_region_here
   ```

## 使用方法

1. アプリケーションを実行します：
   ```
   python app.py
   ```

2. ウェブブラウザで`http://localhost:5000`にアクセスします。

3. テキストエリアにプロンプトを入力し、「生成」ボタンをクリックします。

4. 生成されたHTMLコンテンツが表示されます。

## ファイル構成

- `app.py`: Flaskアプリケーションのメインファイル
- `templates/index.html`: メインページのテンプレート（プロンプト入力フォーム、生成結果表示、HTMLプレビューを含む）
- `requirements.txt`: 必要なPythonパッケージのリスト
- `.env`: AWS認証情報を含む環境変数ファイル（gitignoreに追加することを推奨）

## EC2でのデプロイ

EC2インスタンスでこのアプリケーションを実行する手順は以下の通りです：

1. EC2インスタンスを起動する:
   - Amazon Linux 2 AMIを選択してください。
   - セキュリティグループで80番ポート（HTTP）を開放してください。

2. EC2インスタンスに接続:
   - (SSHを使用して)インスタンスに接続します。

3. 必要なソフトウェアのインストール:
   ```
   sudo yum update -y
   sudo yum install -y httpd python3 python3-pip git
   ```

4. アプリケーションのクローン:
   ```
   git clone [your-repository-url]
   cd [your-repository-name]
   ```

5. 必要なPythonパッケージのインストール:
   ```
   pip3 install -r requirements.txt
   ```

6. アプリケーションの設定:
   - `.env`ファイルを作成し、必要な環境変数を設定します。

7. Apache の設定:
   - Apache設定ファイルを編集して、FlaskアプリケーションをWSGIとして実行するように設定します。
   ```
   sudo nano /etc/httpd/conf.d/flaskapp.conf
   ```
   以下の内容を追加します：
   ```
   <VirtualHost *:80>
     ServerName [your-domain-or-ip]
     WSGIDaemonProcess flaskapp user=ec2-user group=ec2-user threads=5
     WSGIScriptAlias / /var/www/flaskapp/flaskapp.wsgi

     <Directory /var/www/flaskapp>
       WSGIProcessGroup flaskapp
       WSGIApplicationGroup %{GLOBAL}
       Order deny,allow
       Allow from all
     </Directory>
   </VirtualHost>
   ```
    - 詳細な情報と確認方法については、[Apache設定の詳細](Apache設定の詳細.md)を参照してください。

8. WSGIファイルの作成:
   ```
   sudo mkdir /var/www/flaskapp
   sudo nano /var/www/flaskapp/flaskapp.wsgi
   ```
   以下の内容を追加します：
   ```python
   import sys
   sys.path.insert(0, '/path/to/your/application')

   from app import app as application
   ```

9. Apache サービスの開始:
   ```
   sudo systemctl start httpd
   sudo systemctl enable httpd
   ```

10. ウェブサイトにアクセス:
    - ブラウザでEC2インスタンスのパブリックIPアドレスまたはパブリックDNS名を開きます。

## 注意事項

- このコードはデモンストレーション用です。本番環境での使用には、セキュリティ強化やエラーハンドリングの改善が必要です。
- 生成AIの出力をそのまま表示することにはセキュリティリスクがあります。実際の実装では、出力のサニタイズや制限を検討してください。
- AWSの認証情報を適切に管理し、`.env`ファイルをバージョン管理システムにコミットしないよう注意してください。
- EC2インスタンスにAmazon Bedrockへのアクセス権限を持つIAMロールを割り当てることを忘れずに。

## ライセンス

このプロジェクトは[MITライセンス](https://opensource.org/licenses/MIT)の下で公開されています。

## 貢献

バグの報告や機能の提案は、Issueを作成してください。プルリクエストも歓迎します。

## サポート

質問や支援が必要な場合は、Issueを作成するか、プロジェクトの管理者に直接連絡してください。