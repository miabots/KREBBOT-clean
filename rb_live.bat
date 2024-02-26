powershell -Command "$Env:APP_ENV='live'; & docker-compose -p live -f docker-compose.live.yml down"
powershell -Command "$Env:APP_ENV='live'; & docker-compose -p live -f docker-compose.live.yml build"
powershell -Command "$Env:APP_ENV='live'; & docker-compose -p live -f docker-compose.live.yml up -d"