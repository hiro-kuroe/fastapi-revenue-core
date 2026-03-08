# Stripe / FastAPI トラブル診断フォーム

Stripe決済やサブスクリプション機能に関する問題の診断依頼フォームです。

以下のような問題の調査・診断を受け付けています。

- Stripe Webhook が発火しない  
- サブスク状態が更新されない  
- Checkout は成功しているのにユーザー権限が変わらない  
- 解約後も有料機能が使えてしまう  

送信内容を確認後、対応可否と次のステップをご連絡します。

---

## 1. 現在発生している問題の種類

- Stripe Checkout  
- Stripe Webhook  
- サブスク状態管理  
- 決済ロジック  
- API認証  
- その他

---

## 2. どのような問題が起きていますか？

例

- Webhook が発火しない  
- サブスク状態が更新されない  
- 決済後もユーザーが FREE のまま  
- 解約してもアクセス権が残る  

問題の詳細を記入してください。

---

## 3. 使用しているバックエンドフレームワーク

- FastAPI  
- Django  
- Node.js  
- Laravel  
- その他

---

## 4. 使用しているデータベース

- PostgreSQL  
- MySQL  
- SQLite  
- 不明

---

## 5. Stripeのモード

- Test mode  
- Live mode

---

## 6. 関連しているWebhookイベント

例


checkout.session.completed
customer.subscription.created
invoice.payment_succeeded


---

## 7. エラーメッセージ

エラーログやスクリーンショットがあれば貼り付けてください。

例


Webhook signature verification failed


---

## 8. 関連するコード

可能であれば以下を共有してください。

- Checkout Session 作成コード  
- Webhook ハンドラーコード  
- GitHubリポジトリリンク  

コードまたはリポジトリURL

---

## 9. 緊急度

- 高め（可能な範囲で早めの対応希望）  
- 通常  
- 急ぎではない  

---

## 10. 希望するサポート内容

- 原因診断のみ  
- バグ修正・実装サポート  
- まだ分からない

---

## 11. 連絡先

メール / Discord / Slack など  
連絡可能な情報を記入してください。

---

## 確認メッセージ

送信ありがとうございます。

内容を確認後、対応可否と次のステップをご連絡します。

必要に応じて、追加ログやコードの共有をお願いする場合があります。