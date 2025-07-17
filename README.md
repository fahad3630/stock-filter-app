
# Stock Filter App

تطبيق ويب لفلترة الأسهم الأمريكية والسعودية بناءً على الشروط التالية:
- الإغلاق > EMA7 > EMA20 > EMA50
- RSI > 50
- ROC > 0

## التشغيل
```bash
pip install -r requirements.txt
streamlit run app.py
```

## الملف
- `stocks.xlsx`: يحتوي على رموز الأسهم (يمكنك التعديل عليه)
