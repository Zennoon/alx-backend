import { createClient } from 'redis';

async function createRedisClient () {
  createClient().on('connect', () => {
    console.log('Redis client connected to the server');
  }).on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
  });
}

createRedisClient();
