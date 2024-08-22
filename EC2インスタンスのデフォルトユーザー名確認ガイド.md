# EC2インスタンスのデフォルトユーザー名確認ガイド

EC2インスタンスのデフォルトユーザー名は、使用しているAMI（Amazon Machine Image）によって異なります。以下に、確認方法と主なAMIのデフォルトユーザー名を示します。

## デフォルトユーザー名の確認方法

1. EC2インスタンスに接続する際に使用したユーザー名を確認します。

2. インスタンスに接続後、以下のコマンドを実行して現在のユーザー名を確認できます：
   ```
   whoami
   ```

3. または、以下のコマンドでホームディレクトリを確認することもできます：
   ```
   echo $HOME
   ```

## 主なAMIのデフォルトユーザー名

- Amazon Linux 2 または Amazon Linux AMI: `ec2-user`
- Ubuntu AMI: `ubuntu`
- Debian AMI: `admin` または `root`
- CentOS AMI: `centos`
- RHEL (Red Hat Enterprise Linux) AMI: `ec2-user` または `root`
- SUSE Linux: `ec2-user` または `root`
- Fedora: `fedora` または `ec2-user`
- Bitnami: `bitnami`

## 注意点

- 最新の情報は、使用しているAMIのドキュメントで確認することをお勧めします。
- カスタムAMIを使用している場合、ユーザー名が上記と異なる可能性があります。
- rootユーザーでの直接ログインは、セキュリティ上の理由から通常無効化されています。

## ユーザー名の変更方法

Apache設定ファイル（`/etc/httpd/conf.d/flaskapp.conf`）内のユーザー名を変更する場合：

1. 設定ファイルを開きます：
   ```
   sudo nano /etc/httpd/conf.d/flaskapp.conf
   ```

2. 以下の行を探し、適切なユーザー名に変更します：
   ```
   WSGIDaemonProcess flaskapp user=ec2-user group=ec2-user threads=5
   ```

3. 例えば、Ubuntuを使用している場合：
   ```
   WSGIDaemonProcess flaskapp user=ubuntu group=ubuntu threads=5
   ```

4. 変更を保存し、Apacheを再起動します：
   ```
   sudo systemctl restart httpd
   ```

適切なユーザー名を使用することで、Apacheが正しい権限でFlaskアプリケーションを実行できるようになります。