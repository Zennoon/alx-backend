import { createClient, print } from 'redis';

function createRedisClient () {
  const client = createClient().on('connect', () => {
    console.log('Redis client connected to the server');
  }).on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
  });

  return client;
}