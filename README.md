
# RMS（Refrigerator Management System）


[![Product Name](image.png)](https://www.youtube.com/watch?v=G5rULR53uMk)

## 製品概要
### 冷蔵庫 x Tech

### 背景（製品開発のきっかけ、課題等）
農林水産省によると，まだ食べられるのに廃棄している食品，
いわゆる食品ロスの量は年間621万トンと報告されています．
その約半数は家庭から出された食品です．

食品ロスは環境問題にも影響を及ぼし，また金銭的にも家系を圧迫してしまいます．
食品の廃棄理由の主な原因は期限切れであると言われています．
その結果，消費者が使い切れず廃棄する食品が数多く存在します．
そこで，消費者が食品をきちんと使い切るために
冷蔵庫の食品の期限を知ることが必要であると考え，
我々はRMSを作りました．

### 製品説明（具体的な製品の説明）
システムの動作概要を下記に示す，
-----
1. 冷蔵庫に食品を入れる前に登録
2. 冷蔵庫の中身（登録した食品）を適宜確認可能
3. 賞味期限が近くなった商品をLINEbotが通知
-----

LINEのアプリ上で登録ボタンを押すと，
商品を特定するために
バーコードを認識するWebページに遷移します．
ユーザが食品のバーコードを認識させることで，
システムが食品名と画像を自動で取得します．
その後，ユーザは食品の賞味期限を入力し，
食品名と食品画像，食品の賞味期限を登録します．

LINEのアプリ上で一覧ボタンを押すと，
登録された食品の情報（食品名，食品の画像，食品の賞味期限）をLINE上で確認することができます．
また，表示された食品を食べたり捨てたりした場合は，
「食べた」ボタンか「捨てた」ボタンを押すことでその食品の情報を削除することができます．

さらに，期限の迫った食品の通知を行います．
期限が迫って来るとLINE上で通知を行い，消費を促します．

### 特長

#### 1. バーコード認識による食品名・食品画像の取得
ユーザがバーコードを撮影するだけで，
が自動的に食品名を特定し画像とともに表示・保存します．

#### 2. 冷蔵庫の中の食品管理
登録した食品の一覧をいつでも確認することができるので，
ユーザは冷蔵庫内にどんな食品があるのかを把握し，買いすぎることがなくなります．

#### 3. 期限の迫った食品の通知
食品の賞味期限が迫って来るとLINE上で通知するので，
ユーザは賞味期限を再認識することができ，食品を捨てずに使い切ることができます．

### 解決出来ること
ユーザは冷蔵庫にある食品やその賞味期限を確認することができるので，
食品を捨てることなくきちんと使い切ることができます．
それにより，食品を廃棄することでの生じる環境問題を解決します．
さらに，食品の無駄がなくなることにより，
家計での食費の削減にも繋がります．

### 今後の展望
* 賞味期限の自動認識
* Clovaとの連携することにより，音声により通知を実施

## 開発内容・開発技術
### 活用した技術
#### API・データ
* LINE manager
* AWS API Gateway
* google画像検索

#### フレームワーク・ライブラリ・モジュール
* AWS (API Gateway, Lambda, DynamoDB, S3)

#### デバイス
* スマートフォン
* PC
* タブレット

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* バーコード情報から商品情報と商品の画像を取得
* LINEbotを用いた商品一覧の表示
* 賞味期限が近くなった食品の通知
