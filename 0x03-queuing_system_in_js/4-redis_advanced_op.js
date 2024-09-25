import { createClient, print } from 'redis';

const client = createClient().on('connect', () => {
  console.log('Redis client connected to the server');
}).on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const schools = [
  { Portland: 50 },
  { Seattle: 80 },
  { 'New York': 20 },
  { Bogota: 20 },
  { Cali: 40 },
  { Paris: 2 }
];

for (const school of schools) {
  client.hset('HolbertonSchools', Object.keys(school)[0], Object.values(school)[0], print);
}

client.hgetall('HolbertonSchools', (err, res) => {
  if (!err) {
    console.log(res);
  }
});
