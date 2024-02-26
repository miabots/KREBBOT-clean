# Line 1: Shut down services
export APP_ENV=beta; docker-compose -p beta -f docker-compose.beta.yml down

# Line 2: Build images
export APP_ENV=beta; docker-compose -p beta -f docker-compose.beta.yml build

# Line 3: Start services
export APP_ENV=beta; docker-compose -p beta -f docker-compose.beta.yml up -d