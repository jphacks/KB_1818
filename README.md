
# RMS（Refrigerator Management System）


[![Product Name](image.png)](https://youtu.be/_xNq3bSqzqY)

## 製品概要
### 冷蔵庫 x Tech

### 背景（製品開発のきっかけ、課題等）
農林水産省によると，まだ食べられるのに廃棄している食品，
いわゆる食品ロスの量は年間621万トンと報告されています．
その約半数は家庭から出された食品です．

食品ロスは環境問題にも影響を及ぼし，また金銭的にも家系を圧迫してしまいます．
食品の廃棄理由の主な原因は期限切れであると言われています．
そこで，消費者が食品をきちんと使い切るために
冷蔵庫に入っている食品の期限を知ることが必要であると考え，
我々はRMSを作りました．

### 製品説明（具体的な製品の説明）
システムの動作概要を下記に示します.
-----
1. 冷蔵庫に入れる食品の情報を登録
2. 冷蔵庫の中身（登録した食品）をLineBotにより適宜確認
3. 期限が近くなった食品をLINEbotが通知
-----
#### 食品情報の登録
LINEのアプリ上で登録ボタンを押すと，
商品を特定するために
バーコードを認識するWebページに遷移します．
ユーザは端末のカメラでバーコードを撮影します．
撮影した食品のバーコードを用いて，
システムが食品名と画像を自動で取得します．
その後，ユーザは食品の賞味期限を入力し，
食品名と食品画像，食品の賞味期限を登録します．
#### 食品情報の取得
LINEのアプリ上で一覧ボタンを押すと，
登録された食品の情報（食品名，食品の画像，食品の賞味期限）をLINEのアプリ上で確認することができます．
また，表示された食品を食べたり捨てたりした場合は，
「食べた」ボタンか「捨てた」ボタンを押すことでその食品の情報を削除することができます．
#### 賞味期限が近くなった食品の通知
期限が近くなった食品の通知を行います．
期限が近くなるとLINE上で通知を行い，消費を促します．

### 特長

#### 1. バーコード認識による食品名・食品画像の取得
ユーザがバーコードを撮影するだけで，
システムが自動的に食品名を特定し画像とともに表示・保存します．

#### 2. 冷蔵庫の中の食品管理
ユーザは登録した食品の一覧をいつでも確認することができるので，冷蔵庫内の食品と食品の期限を把握し，買いすぎと廃棄を防ぐことができます．

#### 3. 期限の近づいた食品の通知
食品の期限が近づくとLINEのアプリ上で通知するので，
ユーザは期限を再認識することができ，食品を捨てずに使い切ることができます．

### 解決出来ること
ユーザは冷蔵庫にある食品やその賞味期限を確認することができるので，
食品を捨てることなくきちんと使い切ることができます．
それにより，食品を廃棄することでの生じる環境問題を解決します．
さらに，食品の無駄がなくなることにより，
家計での食費の削減にも繋がります．

### 今後の展望
* 賞味期限を画像処理などを用いて自動認識
* Clovaとの連携することにより，音声により通知を実施

## 開発内容・開発技術
### 活用した技術
#### API・データ
* [MessageAPI](https://developers.line.me/ja/services/messaging-api/)
* 商品のバーコード
* google画像検索

#### フレームワーク・ライブラリ・モジュール
* [AWS](https://aws.amazon.com/jp/) (API Gateway, Lambda, DynamoDB, S3)
* [LINE Front-end Framework](https://developers.line.me/ja/docs/liff/)：lineからブラウザの呼び出しに利用
* [JOB](https://github.com/EddieLa/JOB)：バーコード認識に利用
* [WebRTC](https://webrtc.org/)：ブラウザからカメラへのアクセスに利用

![システム構成](https://i.imgur.com/WVnFI9B.png)

#### デバイス
* スマートフォン
* タブレット
* PC（商品登録はできないが，一覧表示は可能）

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* バーコード情報から商品情報と商品の画像を取得
* LINEbotを用いた商品一覧の表示
* 賞味期限が近くなった食品の通知
