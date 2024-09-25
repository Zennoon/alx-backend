import { createClient, print } from 'redis';

function createRedisClient () {
  const client = createClient().on('connect', () => {
    console.log('Redis client connected to the server');
  }).on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
  });

  return client;
}

const client = createRedisClient();

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, print);
};

const displaySchoolValue = (schoolName) => {
  client.get(schoolName, (err, res) => {
    if (!err) {
      console.log(res);
    }
  });
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
