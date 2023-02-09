#### МЕГА КРЕЙЗИ ЗАПУСК

#### Для начала
Создать файл **.env** в корне проекта, и поместить туда содержимое файла **.test.env**
Так же этот же файл скопировать в папку frontend


#### Запуск docker
При запуске создаётся 4 контейнера: postgresql, django, nuxtjs, nginx. Запустить сборку можно командой:
```shell script
docker-compose -f docker-compose-dev.yml up --build -d
лог django: docker-compose -f docker-compose-dev.yml logs django
лог фронта: docker-compose -f docker-compose-dev.yml logs nuxt
```
#### В браузере
```lin
http://localhost:9001 - nuxtjs
http://localhost:9000/(admin/static/graphql) - django
```

#### Что в сборке?
В **nuxtjs** находятся самые необходимые компоненты для работы с django и адаптивом:
- [@nuxtjs/apollo](https://github.com/nuxt-community/apollo-module)
- [@nuxtjs/dotenv](https://github.com/nuxt-community/dotenv-module)
- [@nuxtjs/device](https://github.com/nuxt-community/device-module)
- [bootstrap-vue](https://bootstrap-vue.js.org/docs)
- [cookie-universal-nuxt](https://github.com/microcipcip/cookie-universal)
- [graphql-tag](https://github.com/apollographql/graphql-tag)
- [less](https://github.com/webpack-contrib/less-loader)