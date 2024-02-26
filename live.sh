# Line 1: Shut down services
export APP_ENV=live; docker-compose -p live -f docker-compose.live.yml down

# Line 2: Build images
export APP_ENV=live; docker-compose -p live -f docker-compose.live.yml build

# Line 3: Start services
export APP_ENV=live; docker-compose -p live -f docker-compose.live.yml up -d