powershell -Command "$Env:APP_ENV='beta'; & docker-compose -p beta -f docker-compose.beta.yml down"
powershell -Command "$Env:APP_ENV='beta'; & docker-compose -p beta -f docker-compose.beta.yml build"
powershell -Command "$Env:APP_ENV='beta'; & docker-compose -p beta -f docker-compose.beta.yml up -d"