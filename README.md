# پروژه چت بات

یک وبسایت برای چت با هوش مصنوعی و قابلیت اضافه کردن اطلاعات برای گرفتن جواب های دقیق تر
نوشته شده بر پایه مدل جی پی تی 3.5 و با بک اند جنگو

## Getting Started

```bash
docker build -t <yout-desired-name>:111111 . 
docker compose up
```

با استفاده از داکر پروژه را بیلد کرده و سپس با استفاده از
فایل docker-compose.yml پروژه را ران کنید

پروژه نیاز به دیتابیس پستگرس به همراه اکستنشن pgvector دارد

## Embedding and Model

پروژه نیاز به api openai دارد و باید از طریق
Environment variable ای به اسم OPENAI_API به برنامه داده شود
